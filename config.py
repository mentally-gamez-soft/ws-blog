"""Define all the existing configuration by environmenet."""


class Config(object):
    """Define the default configuration to load for the application."""

    SECRET_KEY = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Define the production configuration to load for the application."""

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:test_123@localhost:5432/miniblog"
    )


class DevelopmentConfig(Config):
    """Define the development configuration to load for the application."""

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:test_123@localhost:5432/miniblog"
    )


class StagingConfig(Config):
    """Define the pre-production configuration to load for the application."""

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:test_123@localhost:5432/miniblog"
    )


class TestingConfig(Config):
    """Define the tests configuration to load for the application."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:test_123@localhost:5432/miniblog"
    )
