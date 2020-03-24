from typing import Dict
import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DEV_DB_URL')
        or 'postgresql://postgres:{password}@localhost/Customers'
        .format(password=os.getenv('DEV_DB_PASS') or '')
    )


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config: Dict[str, type] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
