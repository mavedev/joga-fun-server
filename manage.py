from app import (
    create_app,
    create_db_connection
)
import os


def main() -> None:
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    db = create_db_connection(app)

    @app.route('/')
    def index() -> str:
        return '<h1>Hello!</h1>'

    app.run()


if __name__ == '__main__':
    main()
