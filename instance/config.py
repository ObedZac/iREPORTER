"""App configuration settings"""
import os


class Config:
    """Parent configuration class method."""
    DEBUG = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    BUNDLE_ERRORS = True
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')


class DevelopmentConfig(Config):
    """
        This defines the development environment of the api app
    """
    PROPAGATE_EXEPTIONS = True
    DEBUG = True
    DATABASE = os.getenv('DATABASE_URL')
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = "dbname='ireporter' host='localhost' port='5432' user='zac' password='calculus3'"


class TestingConfig(Config):
    """Configurations of Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    DATABASE = os.getenv('DATABASE_URL')
    DB_NAME = os.getenv('TEST_DB_NAME')
    DATABASE_URL = "dbname='ireporter_test' host='localhost' port='5432' user='zac' password='calculus3'"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = os.getenv('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    "default": DevelopmentConfig
}
