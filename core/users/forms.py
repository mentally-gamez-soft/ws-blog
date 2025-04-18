"""Define the form to signup users."""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    """Declare the form class for users management."""

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(max=64),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Signup")


class LoginForm(FlaskForm):
    """Declare the user login form."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")
