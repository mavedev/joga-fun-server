from typing import Callable

from flask import (
    make_response,
    current_app,
    Response,
    request,
    jsonify
)
from functools import wraps
from http import HTTPStatus

from jwt.exceptions import DecodeError
from jwt import decode

from app.constants import JSONLike, AuthHeader
from app.model import User

from . import api
from .logic import posts, auth


def token_required(wrapped_func: Callable) -> Callable:
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
            return wrapped_func(current_user, *args, **kwargs)
        except DecodeError:
            return make_response(
                'Bad token',
                HTTPStatus.BAD_REQUEST,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
    return get_wrapped


@api.route('/posts/<int:how_many>', methods=['GET'])
def read_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(how_many)
    ])


@api.route('/posts/create', methods=['POST'])
@token_required
def create_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result: bool = posts.create_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/update', methods=['PUT'])
@token_required
def update_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result: bool = posts.update_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/delete', methods=['DELETE'])
@token_required
def delete_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result: bool = posts.delete_post(
        title=body['title']
    )
    return Response(status=200 if result else 500)


@api.route('/auth/login', methods=['POST'])
def login() -> Response:
    body: AuthHeader = request.authorization or {
        'username': '',
        'password': ''
    }
    user: User = auth.get_user(
        body['username'],
        body['password']
    )
    if not user:
        return make_response(
            'Could not verify.',
            HTTPStatus.UNAUTHORIZED,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )
    else:
        return auth.get_token(user.id)
