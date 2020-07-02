import os

from flask_login import LoginManager
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_security import Security, SQLAlchemyUserDatastore

from app import create_app
from app.model import db, User, Post, Role


def main() -> None:
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')

    manager = Manager(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore)
    manager.add_command('db', MigrateCommand)
    manager.add_command(
        'shell',
        Shell(make_context=lambda: {
            'db': db,
            'app': app,
            'User': User,
            'Post': Post,
            'manager': manager,
            'migrate': migrate,
            'security': security,
            'datastore': datastore,
            'login_manager': login_manager
        })
    )

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        return db.session.query(User).get(user_id)

    @manager.command
    def automanage():
        # Comment-like type annotation to avoid manager bugs.
        # type: () -> None
        db.drop_all()
        db.create_all()
        datastore.create_user(username='admin')
        datastore.create_role(
            name='admin',
            description='Site administrator'
        )
        admin_user: User = User.query.first()
        admin_role: Role = Role.query.first()
        datastore.add_role_to_user(admin_user, admin_role)

        password = ''
        while not password:
            password = input('Enter password for admin: ')
        admin_user.set_password(password)

        db.session.commit()

    manager.run()


if __name__ == '__main__':
    main()
