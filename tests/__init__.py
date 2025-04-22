"""Declare the base test classfor the tests suit."""

import unittest

from core import create_app, db
from core.users.models import User


class BaseTestClass(unittest.TestCase):
    """Define the base test class."""

    def setUp(self):
        """Define the data set create before each test."""
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
            # Creamos un usuario administrador
            BaseTestClass.create_user("admin", "admin@xyz.com", "1111", True)
            # Creamos un usuario invitado
            BaseTestClass.create_user("guest", "guest@xyz.com", "1111", False)

    def tearDown(self):
        """Destroy the data set after each test."""
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, email, password, is_admin):
        """Define an utility method to initiate the dataset.

        Args:
            name (str): the name for a user
            email (str): the email of a user
            password (str): a password for a user
            is_admin (bool): indicate if the user is an admin

        Returns:
            User: Returns an instance of a user
        """
        user = User(name, email)
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user

    def login(self, email, password):
        """Declare a utility method to login a user.

        Args:
            email (str): the eail of the user
            password (str): the password for a user

        Returns:
            _type_: _description_
        """
        return self.client.post(
            "/login",
            data=dict(email=email, password=password),
            follow_redirects=True,
        )
