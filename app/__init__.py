from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

__all__ = [
    'create_app'
]


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app


def create_db_connection(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app)
