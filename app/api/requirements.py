from typing import Callable
from functools import wraps

from flask import (
    make_response,
    current_app,
    request
)

from http import HTTPStatus

from jwt.exceptions import DecodeError
from jwt import decode

from app.model import User


def token_required(*, of: str) -> Callable:
    """A decorator requiering the JSON access token.
       Args:
           of (str): of which role the token must be.
    """
    def get_outer(wrapped_func: Callable) -> Callable:
        @wraps(wrapped_func)
        def get_wrapped(*args, **kwargs) -> Callable:
            token: bytes = b''
            if 'x-access-token' not in request.headers:
                return make_response(
                    'Need authorization',
                    HTTPStatus.UNAUTHORIZED,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            try:
                token = request.headers['x-access-token']
                data = decode(token, current_app.config['SECRET_KEY'])
                current_user = User.query.filter_by(id=data['user_id']).first()
                if _check_role(of, current_user):
                    return wrapped_func(current_user, *args, **kwargs)
                else:
                    return make_response(
                        'Permission denied',
                        HTTPStatus.FORBIDDEN,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'}
                    )
            except DecodeError:
                return make_response(
                    'Bad token',
                    HTTPStatus.BAD_REQUEST,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
        return get_wrapped
    return get_outer


def _check_role(role: str, user: User,) -> bool:
    return role in user.roles
