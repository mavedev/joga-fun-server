import os

from flask_script import Manager, Shell

from app import create_app
from app.model import db, User, Post

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command(
    'shell',
    Shell(make_context=lambda: {
        'app': app,
        'db': db,
        'User': User,
        'Post': Post
    })
)


def main() -> None:
    manager.run()


if __name__ == '__main__':
    main()
