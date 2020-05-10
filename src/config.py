import os

basedir = os.path.abspath(os.path.dirname(__file__))
dummy_database = "sqlite:///test.db"
database_name = "flask_jwt_auth"


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = "sqlite:///unittest_db.db"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
