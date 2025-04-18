"""Define the routes for the blog post module."""

from flask import abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from core.blog_post.models import Post

from . import blog_post_bp
from .forms import BlogPostForm


@blog_post_bp.route("/")
def index():
    """Declare the index route.

    Returns:
        str: All the existing posts.
    """
    posts = Post.get_all()
    return render_template("index.html", posts=posts)


@blog_post_bp.route("/post/<string:slug>/")
def show_post(slug):
    """Show a post by its slug.

    Args:
        slug (str): The title of the post as slug.

    Returns:
        str: The post title.
    """
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)


@blog_post_bp.route(
    "/admin/post/", methods=["GET", "POST"], defaults={"post_id": None}
)
@blog_post_bp.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_form(post_id):
    """Define the form to consult a post and to modify it.

    Args:
        post_id (int, optional): The id of the post. Defaults to None.

    Returns:
        str: Indicate the id of the post.
    """
    form = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        return redirect(url_for("blog_post.index"))
    return render_template("admin/post_form.html", form=form)
