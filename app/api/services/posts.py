from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.model import db, Category, Post


def create_post(title: str, body: str, image: str, category_name: str) -> bool:
    """Try to create a post in the DB with the given title and body
       and then connect it to the category with the given name.
       Returns:
           The return value. True for success, False otherwise.
    """
    try:
        category = Category.query.filter(
            Category.name == category_name
        ).first()
        db.session.add(Post(
            title=title,
            body=body,
            image_url=image,
            category=category
        ))
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def read_posts(chunk: int) -> List[Post]:
    """Retrieve n last posts from the DB."""
    try:
        return db.session.query(Post).all()
    except SQLAlchemyError:
        return []


def update_post(title: str, body: str, image: str) -> bool:
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
            target_post.image_url = image
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


def get_posts_quantity() -> int:
    return db.session.query(Post).count()
