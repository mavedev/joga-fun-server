from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.model import db, Post


def create_post(title: str, body: str) -> bool:
    """Try to create a post in the DB with the given title and body.
       Returns:
           The return value. True for success, False otherwise.
    """
    try:
        db.session.add(Post(title=title, body=body))
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def read_posts(how_many: int) -> List[Post]:
    """Retrieve n last posts from the DB."""
    return db.session.query(Post).limit(how_many).all()


def update_post(title: str, body: str) -> bool:
    """Try to update the body for the post with the given title.
       Returns:
           The return value. True for success, False otherwise.
    """
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


def delete_post(title: str) -> bool:
    """Try to delete the post with the given title.
       Returns:
           The return value. True for success, False otherwise.
    """
    target_post: Post = (
        db.session.query(Post)
        .filter(Post.title == title)
        .first()
    )

    if not target_post:
        return False
    else:
        try:
            db.session.delete(target_post)
            db.session.commit()
            return True
        except SQLAlchemyError:
            return False
