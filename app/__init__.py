from flask import Flask
from config import config


def get_app(config_name: str) -> Flask:
    app = Flask(__file__)
    app.config.from_object(config[config_name])
    return app
