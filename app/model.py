from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .constants import (
    JSONLike,
    TEXT_LEN_MAX,
    TEXT_LEN_MID,
    TEXT_LEN_MIN
)

db = SQLAlchemy()


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Category(db.Model):  # type: ignore
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(TEXT_LEN_MID), nullable=False, unique=True)
    posts = db.relationship('Post', backref='category')

    def __repr__(self) -> str:
        return '<Category {}>'.format(self.name)

    def to_json(self) -> JSONLike:
        return {
            'name': self.name
        }


class Post(db.Model):  # type: ignore
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(TEXT_LEN_MID))
    image_url = db.Column(db.Text)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    comments = db.relationship('Comment', backref='post')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.title)

    def to_json(self) -> JSONLike:
        return {
            'title': self.title,
            'body': self.body,
            'imageURL': self.image_url,
            'created': self.created,
            'category': self.category.name
        }


class Comment(db.Model):  # type: ignore
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(TEXT_LEN_MID), nullable=False)
    email = db.Column(db.String(TEXT_LEN_MAX), nullable=False)
    site = db.Column(db.String(TEXT_LEN_MAX))
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self) -> str:
        return '<Comment of {}>'.format(self.author)

    def to_json(self) -> JSONLike:
        return {
            'author': self.author,
            'email': self.email,
            'site': self.site,
            'body': self.body
        }


class Role(db.Model, RoleMixin):  # type: ignore
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(TEXT_LEN_MIN), unique=True)
    description = db.Column(db.String(TEXT_LEN_MAX))

    def __repr__(self) -> str:
        return '<Role {}>'.format(self.name)

    def to_json(self) -> JSONLike:
        return {
            'name': self.name
        }


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(TEXT_LEN_MIN), nullable=False, unique=True)
    password_hash = db.Column(
        db.String(TEXT_LEN_MID),
        nullable=False,
        default=''
    )
    active = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('user', lazy='dynamic')
    )

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<{}:{}>".format(self.id, self.username)
