"""Defines the models for the users module."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin):
    """Declare the user model class."""

    def __init__(self, id, name, email, password, is_admin=False):
        """Creqte qn instance for a user.

        Args:
            id (int): The ID for a user.
            name (str): the name of a suer.
            email (str): the email of a user.
            password (str): the password of the user.
            is_admin (bool, optional): Indicate if a user has admin privileges. Defaults to False.
        """
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password):
        """Set the assword for a user.

        Args:
            password (str): the chosen password.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Control that a given password is correct.

        Args:
            password (str): the password t ocheck.

        Returns:
            bool: True if the given password is the same as the stored one, False otherwise.
        """
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        """Set the representation of an instance of a user.

        Returns:
            str: An instance of a user.
        """
        return "<User {}>".format(self.email)


users = []


def get_user(email) -> "User" | None:
    """Retrieve an instance of a user according to its email.

    Returns:
        User: an instance of a user. None if the email refers to no user.
    """
    for user in users:
        if user.email == email:
            return user
    return None
