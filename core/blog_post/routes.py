"""Define the routes for the blog post module."""

import logging

from flask import (
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from core.blog_post.models import Comment, Post
from core.blog_post.templates.forms import CommentForm
from core.users.decorators import admin_required
from core.users.models import User

from . import blog_post_bp
from .forms import BlogPostForm, UserAdminForm

logger = logging.getLogger(__name__)


@blog_post_bp.route("/")
def index():
    """Declare the index route.

    Returns:
        str: the paginated list of blog posts.
    """
    current_app.logger.info("Mostrando los posts del blog")
    logger.info("Mostrando los posts del blog")
    page = int(request.args.get("page", 1))
    per_page = current_app.config["ITEMS_PER_PAGE"]
    post_pagination = Post.all_paginated(page, per_page)
    return render_template("index.html", post_pagination=post_pagination)


@blog_post_bp.route("/post/<string:slug>/")
def show_post(slug):
    """Show a post by its slug.

    Args:
        slug (str): The title of the post as slug.

    Returns:
        str: The post title.
    """
    logger.info("Mostrando un post")
    logger.debug(f"Slug: {slug}")
    post = Post.get_by_slug(slug)
    if not post:
        logger.info(f"El post {slug} no existe")
        abort(404)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(
            content=content,
            user_id=current_user.id,
            user_name=current_user.name,
            post_id=post.id,
        )
        comment.save()
        return redirect(url_for("blog_post.show_post", slug=post.title_slug))
    return render_template("post_view.html", post=post, form=form)


@blog_post_bp.route("/admin/post/", methods=["GET", "POST"])
@login_required
@admin_required
def post_form():
    """Define the form to create a new post.

    Returns:
        str: Indicate the id of the post.
    """
    form = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        logger.info(f"Guardando nuevo post {title}")
        return redirect(url_for("blog_post.list_posts"))
    return render_template("admin/post_form.html", form=form)


@blog_post_bp.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
@admin_required
def update_post_form(post_id):
    """Define the form to modify a blog post.

    Args:
        post_id (int, optional): The id of the post. Defaults to None.

    Returns:
        str: Indicate the id of the post.
    """
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f"El post {post_id} no existe")
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        logger.info(f"Guardando el post {post_id}")
        return redirect(url_for("blog_post.list_posts"))
    return render_template("admin/post_form.html", form=form, post=post)


@blog_post_bp.route("/admin/posts/")
@login_required
@admin_required
def list_posts():
    """_sumDescribe the view to get the list of posts."""
    posts = Post.get_all()
    return render_template("admin/posts.html", posts=posts)


@blog_post_bp.route("/error")
def show_error():
    """Create a route to demonstrate the display of an error."""
    res = 1 / 0
    posts = Post.get_all()
    return render_template("blog_post/index.html", posts=posts)


@blog_post_bp.route(
    "/admin/post/delete/<int:post_id>/",
    methods=[
        "POST",
    ],
)
@login_required
@admin_required
def delete_post(post_id):
    """Describe the view to delete a blog post."""
    logger.info(f"Se va a eliminar el post {post_id}")
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f"El post {post_id} no existe")
        abort(404)
    post.delete()
    logger.info(f"El post {post_id} ha sido eliminado")
    return redirect(url_for("blog_post.list_posts"))


@blog_post_bp.route("/admin/user/<int:user_id>/", methods=["GET", "POST"])
@login_required
@admin_required
def update_user_form(user_id):
    """Define the view to edit a user info."""
    # Aquí entra para actualizar un usuario existente
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f"El usuario {user_id} no existe")
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del usuario.
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f"Guardando el usuario {user_id}")
        return redirect(url_for("admin.list_users"))
    return render_template("admin/user_form.html", form=form, user=user)


@blog_post_bp.route(
    "/admin/user/delete/<int:user_id>/",
    methods=[
        "POST",
    ],
)
@login_required
@admin_required
def delete_user(user_id):
    """Define the view to delete a user."""
    logger.info(f"Se va a eliminar al usuario {user_id}")
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f"El usuario {user_id} no existe")
        abort(404)
    user.delete()
    logger.info(f"El usuario {user_id} ha sido eliminado")
    return redirect(url_for("admin.list_users"))
