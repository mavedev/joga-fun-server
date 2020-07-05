from flask import Response, request, jsonify

from app.constants import JSONLike, AuthHeader
from app.model import User

from . import api
from .services import categories, posts, auth
from .misc import (
    authorization_header_required,
    bad_auth_response,
    token_required,
    response_from
)


@api.route('/categories/<int:how_many>', methods=['GET'])
def read_categories(how_many: int) -> str:
    return jsonify(results=[
        categorie.to_json() for categorie in
        categories.read_categories(how_many)
    ])


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
    result = posts.create_post(body['title'], body['body'], body['category'])
    return response_from(result)


@api.route('/posts/update', methods=['PUT'])
@token_required(of='admin')
def update_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result = posts.update_post(body['title'], body['body'])
    return response_from(result)


@api.route('/posts/delete', methods=['DELETE'])
@token_required(of='admin')
def delete_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result = posts.delete_post(body['title'])
    return response_from(result)


@api.route('/auth/login', methods=['POST'])
@authorization_header_required
def login() -> Response:
    body: AuthHeader = request.authorization or {}
    user: User = auth.get_user(body['username'], body['password'])
    if not user:
        return bad_auth_response('Could not verify user.')
    else:
        return auth.get_token(user.id)
