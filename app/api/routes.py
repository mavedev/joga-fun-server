from flask import jsonify, request, Response

from . import api
from . import posts


@api.route('/posts/<int:how_many>')
def read_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        posts.read_posts(how_many)
    ])


@api.route('/posts/create', methods=['POST'])
def create_post() -> str:
    result: bool = posts.create_post(
        title=request['title'],
        body=request['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/update', methods=['POST'])
def update_post() -> str:
    result: bool = posts.update_post(
        title=request['title'],
        body=request['body']
    )
    return Response(status=200 if result else 500)


@api.route('/posts/delete', methods=['DELETE'])
def delete_post() -> str:
    result: bool = posts.delete_post(
        title=request['title']
    )
    return Response(status=200 if result else 500)
