"""Declare the module of the application."""

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()


def register_blueprints(app):
    """Register all the blue prints of the entry points.

    Args:
        app (_type_): the flask app.

    Returns:
        app: the flask app.
    """
    # Registro de los Blueprints
    from .users import users_bp

    app.register_blueprint(users_bp)

    from .blog_post import blog_post_bp

    app.register_blueprint(blog_post_bp)


def create_app():
    """Create the application loading the config.

    Returns:
        app: the flask application.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:test_123@localhost:5432/miniblog"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    db.init_app(app)

    register_blueprints(app)

    # Custom error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Add custom error handlers to the app."""

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template("500.html"), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template("404.html"), 404
