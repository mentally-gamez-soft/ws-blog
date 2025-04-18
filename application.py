"""Create the flask application instance and config route."""

from urllib.parse import urlparse

from flask import Flask, abort, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy

from core.blog_post.forms import BlogPostForm
from core.users.forms import LoginForm, SignupForm
from core.users.models import User, users

app = Flask(__name__)
app.config["SECRET_KEY"] = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:test_123@localhost:5432/miniblog"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from core.blog_post.models import Post
from core.users.models import User


@login_manager.user_loader
def load_user(user_id):
    """Load the user session.

    Args:
        user_id (int): The id of the user.

    Returns:
        user: an instance for the logged in user.
    """
    return User.get_by_id(int(user_id))


@app.route("/")
def index():
    """Declare the index route.

    Returns:
        str: All the existing posts.
    """
    posts = Post.get_all()
    return render_template("index.html", posts=posts)


@app.route("/post/<string:slug>/")
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


@app.route("/admin/post/", methods=["GET", "POST"], defaults={"post_id": None})
@app.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
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

        return redirect(url_for("index"))
    return render_template("admin/post_form.html", form=form)


@app.route(
    "/signup/",
    methods=(
        "GET",
        "POST",
    ),
)
def show_signup_form():
    """Define the form for a user to signup."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()
    error = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = (
                f"El email {email} ya está siendo utilizado por otro usuario"
            )
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)

            next_page = request.args.get("next", None)
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("index")
            return redirect(next_page)

    return render_template("users/signup_form.html", form=form, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Define the form for a user to login."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("users/login_form.html", form=form)


@app.route("/logout")
def logout():
    """Log a user out.

    Returns:
        Response: the response to the index page.
    """
    logout_user()
    return redirect(url_for("index"))
