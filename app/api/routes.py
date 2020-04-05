from flask import jsonify, request

from . import api
from .post import get_posts


@api.route('/posts/<int:how_many>')
def get_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        get_posts(how_many)
    ])


@api.route('posts/create', methods=['POST'])
def create_post() -> str:
    pass
