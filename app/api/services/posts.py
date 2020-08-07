from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.constants import POSTS_CHUNK_SIZE
from app.model import db, Category, Post
from app.api.types import PostChunkDTO


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


def read_posts_unfiltered(chunk: int) -> PostChunkDTO:
    """Retrieve posts of a chunk provided from the DB."""
    try:
        results = _get_sorted(db.session.query(Post).all())
        results_chunk = _retrieve_chunk(chunk, results)
        return PostChunkDTO(len(results), results_chunk)
    except SQLAlchemyError:
        return PostChunkDTO(0, [])


def read_posts_filtered(chunk: int, category: str) -> PostChunkDTO:
    """Retrieve posts of a chunk provided from the DB
       filtered by a category provided.
       """
    try:
        results = _get_sorted(db.session.query(Post).all())
        filtered_results = [
            post for post in results
            if post.category.name == category
        ]
        results_chunk = _retrieve_chunk(chunk, filtered_results)
        return PostChunkDTO(len(filtered_results), results_chunk)
    except SQLAlchemyError:
        return PostChunkDTO(0, [])


def _retrieve_chunk(chunk: int, posts: List[Post]) -> List[Post]:
    index_from = POSTS_CHUNK_SIZE * (chunk - 1)
    index_to = POSTS_CHUNK_SIZE * chunk
    return posts[index_from:index_to]


def _get_sorted(posts: List[Post]) -> List[Post]:
    return sorted(posts, key=lambda x: x.created)


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
