from flask import Response, request, jsonify

from app.constants import JSONLike, AuthHeader, POSTS_CHUNK_SIZE
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


@api.route('/posts/<int:chunk>', methods=['GET'])
def read_posts(chunk: int) -> str:
    """Posts are split by five-post chunks.
       Chunk argument is the chunk that must be returned.
    """
    index_from = POSTS_CHUNK_SIZE * (chunk - 1)
    index_to = POSTS_CHUNK_SIZE * chunk
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(chunk)[index_from:index_to]
    ])


@api.route('/posts/filtered/<string:category>/<int:chunk>', methods=['GET'])
def read_posts_filtered(category: str, chunk: int) -> str:
    """Get posts chunk of a category given."""
    index_from = POSTS_CHUNK_SIZE * (chunk - 1)
    index_to = POSTS_CHUNK_SIZE * chunk
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(chunk)
        if post.category.name == category
    ][index_from:index_to])


@api.route('/posts/quantity', methods=['GET'])
def get_posts_quantity() -> str:
    return jsonify(result=posts.get_posts_quantity())


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
