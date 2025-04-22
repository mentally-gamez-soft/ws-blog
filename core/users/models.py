"""Defines the models for the users module."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from core import db


class User(db.Model, UserMixin):
    """Declare the user model class."""

    __tablename__ = "blog_user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email):
        """Declare constructor for User.

        Args:
            name (str): the name of a user
            email (str): the email of a user
        """
        self.name = name
        self.email = email

    def set_password(self, password):
        """Set the assword for a user.

        Args:
            password (str): the chosen password.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Control that a given password is correct.

        Args:
            password (str): the password t ocheck.

        Returns:
            bool: True if the given password is the same as the stored one, False otherwise.
        """
        return check_password_hash(self.password, password)

    def save(self):
        """Save an instance of a user in the database."""
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """Set the representation of an instance of a user.

        Returns:
            str: An instance of a user.
        """
        return f"<User {self.email}>"

    @staticmethod
    def get_by_id(id) -> "User":
        """Retrieve a user according to its ID.

        Args:
            id (int): the ID of a user.

        Returns:
            User: An instance of a user.
        """
        return User.query.get(id)

    @staticmethod
    def get_by_email(email) -> "User":
        """Retrieve a user according to its email.

        Args:
            email (str): the email of a user.

        Returns:
            User: An instance of a user.
        """
        return User.query.filter_by(email=email).first()

    def delete(self):
        """Delete an instance of a user."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Retrieve the list of all the users."""
        return User.query.all()
