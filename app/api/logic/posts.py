from typing import List

from app.model import db, Post


def get_posts(how_many: int) -> List[Post]:
    return db.session.query(Post).limit(how_many).all()
