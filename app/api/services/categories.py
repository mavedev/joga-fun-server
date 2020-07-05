from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.model import db, Category


def create_category(name: str) -> bool:
    """Try to create a category in the DB with the given name.
       Returns:
           The return value. True for success, False otherwise.
    """
    try:
        db.session.add(Category(name=name))
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def read_categories(how_many: int) -> List[Category]:
    """Retrieve n last categories from the DB."""
    try:
        return db.session.query(Category).limit(how_many).all()
    except SQLAlchemyError:
        return []
