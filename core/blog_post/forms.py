"""Declare the forms for managin the blog posts."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
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
    post_image = FileField(
        "Imagen de cabecera",
        validators=[FileAllowed(["jpg", "png"], "Solo se permiten imágenes")],
    )
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class UserAdminForm(FlaskForm):
    """Describe the form to toggle a user as an admin."""

    is_admin = BooleanField("Administrador")
    submit = SubmitField("Guardar")
