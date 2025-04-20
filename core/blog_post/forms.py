"""Declare the forms for managin the blog posts."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class BlogPostForm(FlaskForm):
    """Describe the form for a post on the blog."""

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=255),
        ],
    )
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class UserAdminForm(FlaskForm):
    """Describe the form to toggle a user as an admin."""

    is_admin = BooleanField("Administrador")
    submit = SubmitField("Guardar")
