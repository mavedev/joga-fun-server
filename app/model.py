from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin

db = SQLAlchemy()
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):  # type: ignore
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model):  # type: ignore
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


class Post(db.Model):  # type: ignore
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs) -> None:
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.title)
