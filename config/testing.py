"""Define the tests configuration to load for the application."""

from .default import *

SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:test_123@localhost:5433/miniblog_test"
)
DEBUG = True
TESTING = True
APP_ENV = APP_ENV_TESTING
WTF_CSRF_ENABLED = False
