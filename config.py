from typing import Dict


class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True


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
