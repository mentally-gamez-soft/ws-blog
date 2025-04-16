"""Define the form to signup users."""

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
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
