"""Define the routes for the users module."""

from urllib.parse import urlparse

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from core import login_manager

from . import users_bp
from .forms import LoginForm, SignupForm
from .models import User


@login_manager.user_loader
def load_user(user_id):
    """Load the user session.

    Args:
        user_id (int): The id of the user.

    Returns:
        user: an instance for the logged in user.
    """
    return User.get_by_id(int(user_id))


@users_bp.route(
    "/signup/",
    methods=(
        "GET",
        "POST",
    ),
)
def show_signup_form():
    """Define the form for a user to signup."""
    if current_user.is_authenticated:
        return redirect(url_for("blog_post.index"))

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


@users_bp.route("/login", methods=["GET", "POST"])
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


@users_bp.route("/logout")
def logout():
    """Log a user out.

    Returns:
        Response: the response to the index page.
    """
    logout_user()
    return redirect(url_for("index"))
