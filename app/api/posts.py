from flask import jsonify

from . import api
from ..model import db, Post


@api.route('/posts/<int:how_many>')
def get_posts(how_many: int) -> str:
    return jsonify(results=[
        post.to_json() for post in
        db.session.query(Post).limit(how_many).all()
    ])
