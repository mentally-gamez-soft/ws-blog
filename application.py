"""Create the flask application instance and config route."""

from urllib.parse import urlparse

from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from core.blog_post.forms import BlogPostForm
from core.users.forms import LoginForm, SignupForm
from core.users.models import User, get_user, users

app = Flask(__name__)
app.config["SECRET_KEY"] = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec

login_manager = LoginManager(app)
login_manager.login_view = "login"

posts = []


@login_manager.user_loader
def load_user(user_id):
    """Load the user session.

    Args:
        user_id (int): The id of the user.

    Returns:
        user: an instance for the logged in user.
    """
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@app.route("/")
def index():
    """Declare the index route.

    Returns:
        str: the number of existing posts.
    """
    return render_template("index.html", posts=posts)


@app.route("/post/<string:slug>/")
def show_post(slug):
    """Show a post by its slug.

    Args:
        slug (str): The title of the post as slug.

    Returns:
        str: The post title.
    """
    return render_template("post_view.html", slug_title=slug)


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
        title_slug = form.title_slug.data
        content = form.content.data

        post = {"title": title, "title_slug": title_slug, "content": content}
        posts.append(post)
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
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)

        next = request.args.get("next", None)
        if next:
            return redirect(next)
        return redirect(url_for("index"))

    return render_template("users/signup_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Define the form for a user to login."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
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
