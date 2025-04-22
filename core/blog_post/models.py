"""Defines the models for the posts blog module."""

import datetime
from typing import List

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
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_name = db.Column(db.String)
    comments = db.relationship(
        "Comment",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="asc(Comment.created)",
    )

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
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f"{slugify(self.title)}-{count}"

    # def public_url(self) -> str:
    #     """Return the public url for a blog post.

    #     Returns:
    #         str: the url of the blog post.
    #     """
    #     return url_for("show_post", slug=self.title_slug)

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

    def delete(self):
        """Delete a post blog instance from DB."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        """Retrieve a blog post according to its ID.

        Args:
            id (int): the ID of the blog post.

        Returns:
            Post: a post instance or None if not found.
        """
        return Post.query.get(id)

    @staticmethod
    def all_paginated(page=1, per_page=20):
        """Define the paginaion on the whole list of blog posts.

        Args:
            page (int, optional): The page to get. Defaults to 1.
            per_page (int, optional): The number of posts per page. Defaults to 20.

        Returns:
            Pagination: the pagination object with a result set of posts.
        """
        return Post.query.order_by(Post.created.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )


class Comment(db.Model):
    """Declare the models for a comment on a blog post."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("blog_user.id", ondelete="SET NULL")
    )
    user_name = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self, content, user_id=None, user_name=user_name, post_id=None
    ):
        """Create an instance of a comment.

        Args:
            content (str): the content of the comment.
            user_id (int, optional): the user id owner of the comment. Defaults to None.
            user_name (str, optional): the name of the user letting the comment. Defaults to user_name.
            post_id (int, optional): the blog post id for this comment. Defaults to None.
        """
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        """Define the representtion of a comment in a log."""
        return f"<Comment {self.content}>"

    def save(self):
        """Save an instance of a comment."""
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete an instance of a comment."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        """Retrieve the list of comments linked to a blog post according to its id.

        Args:
            post_id (int): the ID of the blog post.

        Returns:
            list: all the comments as a list.
        """
        return Comment.query.filter_by(post_id=post_id).all()
