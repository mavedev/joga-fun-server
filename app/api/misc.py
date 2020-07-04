from typing import Callable
from functools import wraps

from flask import (
    make_response,
    current_app,
    Response,
    request
)

from http import HTTPStatus

from jwt.exceptions import DecodeError
from jwt import decode

from app.model import User


def authorization_header_required(wrapped_func: Callable) -> Callable:
    """A decorator requiring authorization information included.
       If the authoriztion info is not provided
       returns corresponding response otherwise
       returns the result of the wrapped function.
    """
    @wraps(wrapped_func)
    def get_wrapped(*args, **kwargs) -> Callable:
        if not request.authorization:
            return bad_auth_response('No auth info provided.')
        else:
            return wrapped_func(*args, **kwargs)
    return get_wrapped


def token_required(*, of: str) -> Callable:
    """A decorator requiring the JSON access token.
       Args:
           of (str): of which role the token must be.
    """
    def get_outer(wrapped_func: Callable) -> Callable:
        @wraps(wrapped_func)
        def get_wrapped(*args, **kwargs) -> Callable:
            token: bytes = b''
            if 'x-access-token' not in request.headers:
                return bad_auth_response('Need authorization')
            try:
                token = request.headers['x-access-token']
                data = decode(token, current_app.config['SECRET_KEY'])
                current_user = User.query.filter_by(id=data['user_id']).first()
                if _check_role(of, current_user):
                    return wrapped_func(current_user, *args, **kwargs)
                else:
                    return bad_auth_response('Permission denied')
            except DecodeError:
                return bad_auth_response('Bad token')
        return get_wrapped
    return get_outer


def response_from(
    result: bool,
    when_ok: HTTPStatus = HTTPStatus.OK,
    when_failed: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
) -> Response:
    """Retrieve response depending on the result of any business logic
       operation.
       Args:
           result (bool): the result of the operation we need to get
       response to.
           when_ok (HTTPStatus): what HTTP status return in case of success.
           when_failed (HTTPStatus): what HTTP status return in case of fail.
       Returns:
           The return value: a Response object.
    """
    if result:
        return make_response('Success.', when_ok)
    else:
        return make_response('Failed.', when_failed)


def bad_auth_response(response_message: str) -> Response:
    """Get 401 response with custom message provided.
       Args:
           response_message (str): custom message.
       Returns:
           The return value: generated Response object.
    """
    return make_response(
        response_message,
        HTTPStatus.UNAUTHORIZED,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def _check_role(role: str, user: User) -> bool:
    """Check if the given user has the given role."""
    return role in user.roles
