from flask import Response, request, jsonify, make_response
from http import HTTPStatus

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


@api.route('/categories', methods=['GET'])
def read_categories() -> str:
    return jsonify(results=[
        categorie.to_json() for categorie in
        categories.read_categories()
    ])


@api.route('/categories/create', methods=['POST'])
@token_required(of='admin')
def create_category(current_user: User) -> Response:
    body: JSONLike = request.json
    result = categories.create_category(body['name'])
    return response_from(result)


@api.route('/posts/<string:category>/<int:chunk>', methods=['GET'])
def read_posts(category: str, chunk: int) -> str:
    """Get posts chunk of a category given."""
    if category == 'all':
        result = posts.read_posts_unfiltered(chunk)
    else:
        result = posts.read_posts_filtered(chunk, category)
    return jsonify(
        chunksLeft=result.chunks_left,
        posts=[post.to_json() for post in result.posts]
    )


@api.route('/post/<int:postID>', methods=['GET'])
def read_post(post_id: int) -> str:
    post_found = posts.read_post(post_id)
    if not post_found:
        return make_response(
            'No post with the ID provided.',
            HTTPStatus.NO_CONTENT
        )
    return jsonify(post=post_found.to_json())


@api.route('/posts/create', methods=['POST'])
@token_required(of='admin')
def create_post(current_user: User) -> Response:
    body: JSONLike = request.json
    result = posts.create_post(
        body['title'],
        body['body'],
        body['imageURL'],
        body['category']
    )
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


@api.route('/login', methods=['POST'])
@authorization_header_required
def login() -> Response:
    body: AuthHeader = request.authorization or {}
    user: User = auth.get_user(body['username'], body['password'])
    if not user:
        return bad_auth_response('Could not verify user.')
    else:
        return auth.get_token(user.id)
