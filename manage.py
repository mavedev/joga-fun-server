import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_security import Security, SQLAlchemyUserDatastore

from app import create_app
from app.model import db, User, Post, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore)
manager.add_command('db', MigrateCommand)
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
