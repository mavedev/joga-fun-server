from flask import jsonify

from . import api
from ..model import db  # noqa


@api.route('/posts/<int:how_many>')
def get_posts(how_many: int) -> str:
    return jsonify({
        'name': 'Test',
        'status': 'happy'
    })
