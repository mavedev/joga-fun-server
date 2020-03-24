import os

from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/')
def index() -> str:
    return '<h1>Hello!</h1>'


def main() -> None:
    app.run()


if __name__ == '__main__':
    main()
