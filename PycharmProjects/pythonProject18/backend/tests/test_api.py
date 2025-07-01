import pytest
from datetime import datetime, timedelta
from backend.app import app, db, Seat


@pytest.fixture()
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        db.session.add(Seat(label="A1"))
        db.session.commit()
    return app.test_client()


def test_make_booking(client):
    start = datetime.now().isoformat()
    end = (datetime.now() + timedelta(hours=1)).isoformat()
    res = client.post(
        "/bookings/",
        json={"user_id": 1, "seat_id": 1, "start_time": start, "end_time": end},
    )
    assert res.status_code == 201


def test_conflict(client):
    now = datetime.now()
    # успешно
    client.post(
        "/bookings/",
        json={
            "user_id": 1,
            "seat_id": 1,
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(hours=1)).isoformat(),
        },
    )
    # конфликт
    res = client.post(
        "/bookings/",
        json={
            "user_id": 2,
            "seat_id": 1,
            "start_time": (now + timedelta(minutes=30)).isoformat(),
            "end_time": (now + timedelta(hours=2)).isoformat(),
        },
    )
    assert res.status_code == 409
