from flask import jsonify, request, Response, make_response
from flask_login import login_required
from http import HTTPStatus

from app.constants import JSONLike, AuthHeader
from app.model import User

from . import api
from .logic import posts, auth


@api.route('/posts/<int:how_many>', methods=['GET'])
def read_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(how_many)
    ])


@api.route('/posts/create', methods=['POST'])
@login_required
def create_post() -> Response:
    body: JSONLike = request.json
    result: bool = posts.create_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/update', methods=['PUT'])
@login_required
def update_post() -> Response:
    body: JSONLike = request.json
    result: bool = posts.update_post(
        title=body['title'],
        body=body['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/delete', methods=['DELETE'])
@login_required
def delete_post() -> Response:
    body: JSONLike = request.json
    result: bool = posts.delete_post(
        title=body['title']
    )
    return Response(status=200 if result else 500)


@api.route('/auth/admin', methods=['POST'])
def administrate() -> Response:
    body: AuthHeader = request.authorization or {
        'username': '',
        'password': ''
    }
    admin_user: User = auth.get_user(
        body['username'],
        body['password']
    )
    if not admin_user:
        return make_response(
            'Could not verify.',
            HTTPStatus.UNAUTHORIZED,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )
    else:
        return auth.get_token(admin_user.id)
