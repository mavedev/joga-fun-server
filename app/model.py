from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):  # type: ignore
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs) -> None:
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.title)
