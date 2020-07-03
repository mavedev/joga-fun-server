from typing import Optional

from flask import current_app, jsonify
from jwt import encode as jwt_encode

from app.model import User
from app.constants import JSONLike


def get_token(user_id: int) -> JSONLike:
    jwt_payload = {'user_id': user_id}
    jwt_secret = current_app.config['SECRET_KEY']
    jwt_alogithm = 'HS256'
    jwt_token = jwt_encode(jwt_payload, jwt_secret, jwt_alogithm)
    return jsonify({'token': jwt_token.decode('utf-8')})


def get_user(username: str, password: str) -> Optional[User]:
    admin: User = User.query.filter(User.username == username).first()
    return admin if admin and admin.check_password(password) else None
