from flask import (
    make_response,
    Response,
    request,
    jsonify
)

from http import HTTPStatus

from app.constants import JSONLike, AuthHeader
from app.model import User

from . import api
from .logic import posts, auth
from .requirements import token_required


@api.route('/posts/<int:how_many>', methods=['GET'])
def read_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(how_many)
    ])


@api.route('/posts/create', methods=['POST'])
@token_required(of='admin')
def create_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result: bool = posts.create_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/update', methods=['PUT'])
@token_required(of='admin')
def update_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result: bool = posts.update_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/delete', methods=['DELETE'])
@token_required(of='admin')
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
