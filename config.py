from typing import Dict
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DB_URL_DEV')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_dev'
        .format(password=os.getenv('DB_PASS_DEV') or '')
    )


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DB_URL_TEST')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_test'
        .format(password=os.getenv('DB_PASS_TEST') or '')
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DB_URL_PROD')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_prod'
        .format(password=os.getenv('DB_PASS_PROD') or '')
    )


config: Dict[str, type] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
