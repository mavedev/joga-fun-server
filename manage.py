import os

from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def main() -> None:
    app.run()


if __name__ == '__main__':
    main()
