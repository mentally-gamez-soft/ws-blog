"""Define the local dev configuration to load for the application."""

from .default import *

APP_ENV = APP_ENV_LOCAL

SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:test_123@localhost:5432/miniblog"
)
