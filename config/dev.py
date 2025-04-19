"""Define the development configuration to load for the application."""

from .default import *

SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:test_123@localhost:5432/miniblog"
)
