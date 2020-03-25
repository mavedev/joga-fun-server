from typing import Dict
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DEV_DB_URL')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_dev'
        .format(password=os.getenv('DEV_DB_PASS') or '')
    )


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DEV_DB_URL')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_test'
        .format(password=os.getenv('DEV_DB_PASS') or '')
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DEV_DB_URL')
        or 'postgresql+psycopg2://postgres:{password}@localhost/joga_prod'
        .format(password=os.getenv('DEV_DB_PASS') or '')
    )


config: Dict[str, type] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
