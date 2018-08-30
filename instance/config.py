import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = 'secr3tk3y'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    TESTING = False
