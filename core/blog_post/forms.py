"""Declare the forms for managin the blog posts."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
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
    title_slug = StringField(
        "Title slug",
        validators=[
            Length(max=255),
        ],
    )
    content = TextAreaField("Content")
    submit = SubmitField("Submit")
