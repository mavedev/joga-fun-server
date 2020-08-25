import os
from app import create_app


to_run = create_app(os.getenv('CONFIG') or 'default')
