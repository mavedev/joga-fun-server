from flask import jsonify

from . import api


@api.route('/posts/<int:number>/')
def get_posts(how_many: int) -> str:
    return jsonify({
        'name': 'Ciri',
        'status': 'happy'
    })
