from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from backend.app.routes import api as booking_api
from backend.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    api = Api(app, doc="/swagger", title="Coworking Booking API")
    api.add_namespace(booking_api)

    return app
