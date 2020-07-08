from flask import Flask
from config import config


__all__ = [
    'create_app'
]


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .model import db
    db.init_app(app)

    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .api import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    return app
