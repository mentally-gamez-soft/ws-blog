"""Defines the models for the posts blog module."""

from typing import List

from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError

from core import db


class Post(db.Model):
    """Declare the post model class."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("blog_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)

    def save(self) -> None:
        """Save an instance of a post blog in the database."""
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.title_slug = f"{slugify(self.title)}-{count}"

    def public_url(self) -> str:
        """Return the public url for a blog post.

        Returns:
            str: the url of the blog post.
        """
        return url_for("show_post", slug=self.title_slug)

    @staticmethod
    def get_by_slug(slug) -> "Post":
        """Retrieve a blog post according to its slug.

        Args:
            slug (str): the slug of a post.

        Returns:
            Post: the blog post of this slug.
        """
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all() -> List:
        """Retrieve the list of all the blog posts.

        Returns:
            List: the list of all the blog posts.
        """
        return Post.query.all()

    def __repr__(self):
        """Set the representation of an instance of a post blog.

        Returns:
            str: An instance of a post.
        """
        return f"<Post {self.title}>"
