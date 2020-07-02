from flask import jsonify, request, Response
from flask_login import login_required

from app.constants import JSONLike

from . import api
from .logic import posts


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
