from datetime import datetime
from typing import Optional

# Данные необходимо храните в БД PostgreSQL
# Необходимо реализовать SPA на React


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)
# подключение к БД.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///coworking.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# БД модели

class Seat(db.Model):
    # место
    __tablename__ = "seats"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)


class Booking(db.Model):
    # бронирование
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey("seats.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# Проверка на наличие конфликтов
def has_conflict(seat_id: int, start: datetime, end: datetime, *, exclude: Optional[int] = None) -> bool:
    q = Booking.query.filter(
        Booking.seat_id == seat_id,
        Booking.start_time < end,
        Booking.end_time > start,
    )
    if exclude:
        q = q.filter(Booking.id != exclude)
    return db.session.query(q.exists()).scalar()

# API
api = Api(app, title="Coworking Booking API", version="1.0", doc="/swagger")


booking_model = api.model(
    "Booking",
    {
        "id": fields.Integer(readOnly=True),
        "user_id": fields.Integer(required=True),
        "seat_id": fields.Integer(required=True),
        "start_time": fields.String(required=True, example="2025-07-01T10:00:00"),
        "end_time": fields.String(required=True, example="2025-07-01T12:00:00"),
    },
)

seat_model = api.model(
    "Seat",
    {"id": fields.Integer(readOnly=True), "label": fields.String},
)

ns = api.namespace("bookings", description="create / view / edit")


@ns.route("/")
class BookingList(Resource):
    @ns.marshal_list_with(booking_model)
    def get(self):
        # список бронирований
        return Booking.query.all()

    @ns.expect(booking_model, validate=True)
    @ns.marshal_with(booking_model, code=201)
    def post(self):
        # создание новой брони
        data = api.payload
        start = datetime.fromisoformat(data["start_time"])
        end = datetime.fromisoformat(data["end_time"])
        if has_conflict(data["seat_id"], start, end):
            api.abort(409, "Already taken")
        booking = Booking(
            user_id=data["user_id"],
            seat_id=data["seat_id"],
            start_time=start,
            end_time=end,
        )
        db.session.add(booking)
        db.session.commit()
        return booking, 201


@ns.route("/<int:bid>")
class BookingItem(Resource):
    @ns.marshal_with(booking_model)
    def get(self, bid):
        return Booking.query.get_or_404(bid)

    @ns.expect(booking_model, validate=True)
    @ns.marshal_with(booking_model)
    def put(self, bid):
        # изменение брони
        booking = Booking.query.get_or_404(bid)
        data = api.payload
        start = datetime.fromisoformat(data["start_time"])
        end = datetime.fromisoformat(data["end_time"])
        if has_conflict(data["seat_id"], start, end, exclude=bid):
            api.abort(409, "Already taken")

        booking.user_id = data["user_id"]
        booking.seat_id = data["seat_id"]
        booking.start_time = start
        booking.end_time = end
        db.session.commit()
        return booking

    @staticmethod
    def delete(bid):
        # удаление брони
        booking = Booking.query.get_or_404(bid)
        db.session.delete(booking)
        db.session.commit()
        return "", 204

@api.route("/seats/availability")
class SeatFree(Resource):
    # свободные места - список
    @api.marshal_list_with(seat_model)
    def get(self):

        start = datetime.fromisoformat(request.args["start"])
        end = datetime.fromisoformat(request.args["end"])
        seats = Seat.query.all()
        return [s for s in seats if not has_conflict(s.id, start, end)]


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
