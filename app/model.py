from typing import Dict, Any
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .constants import (
    _TEXT_LEN_MAX,
    _TEXT_LEN_MID,
    _TEXT_LEN_MIN
)

db = SQLAlchemy()


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Post(db.Model):  # type: ignore
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(_TEXT_LEN_MID))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.title)

    def to_json(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'body': self.body,
            'created': self.created
        }


class Comment(db.Model):  # type: ignore
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.String(_TEXT_LEN_MID), nullable=False)
    email = db.Column(db.String(_TEXT_LEN_MAX), nullable=False)
    site = db.Column(db.String(_TEXT_LEN_MAX))


class Role(db.Model, RoleMixin):  # type: ignore
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(_TEXT_LEN_MIN), unique=True)
    description = db.Column(db.String(_TEXT_LEN_MAX))

    def __repr__(self) -> str:
        return '<Role {}>'.format(self.name)


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(_TEXT_LEN_MIN), nullable=False, unique=True)
    password_hash = db.Column(
        db.String(_TEXT_LEN_MID),
        nullable=False,
        default=''
    )
    active = db.Column(db.Boolean())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<{}:{}>".format(self.id, self.username)
