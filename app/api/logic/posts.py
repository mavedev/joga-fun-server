from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.model import db, Post


def create_post(title: str, body: str) -> bool:
    try:
        db.session.add(Post(title=title, body=body))
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def read_posts(how_many: int) -> List[Post]:
    return db.session.query(Post).limit(how_many).all()


def update_post(title: str, body: str) -> bool:
    target_post: Post = (
        db.session.query(Post)
        .filter(Post.title == title)
        .first()
    )

    if not target_post:
        return False
    else:
        try:
            target_post.body = body
            db.session.commit()
            return True
        except SQLAlchemyError:
            return False
