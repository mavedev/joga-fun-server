from datetime import datetime, timedelta
from flask import current_app, jsonify
from flask_security import login_user
from jwt import encode

from app.model import User
from app.constants import (
    JWT_EXP_DELTA_SECONDS,
    JWT_ALGORITHM,
    JSONLike
)


def get_token(user_id: int) -> JSONLike:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_secret = current_app.config['SECRET_KEY']
    jwt_token = encode(payload, jwt_secret, JWT_ALGORITHM)
    return jsonify({'token': jwt_token.decode('utf-8')})


def can_administrate(username: str, password: str) -> bool:
    admin: User = User.query.filter(User.username == username).first()
    if not admin or not admin.check_password(password):
        return False
    else:
        login_user(admin, remember=True)
        return True
