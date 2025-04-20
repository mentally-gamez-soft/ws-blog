"""Declqre the module for the forms to let a comment on a blog post."""

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    """Define the form for a comment on a blog post."""

    content = TextAreaField(
        "Contenido",
        validators=[
            DataRequired(),
        ],
    )
    submit = SubmitField("Comentar")
