"""Declare the module of the application."""

import logging
from logging.handlers import SMTPHandler

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()  # Se crea un objeto de tipo Migrate


def verbose_formatter():
    """Define the logger formatter for the console."""
    return logging.Formatter(
        "[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )


def mail_handler_formatter():
    """Define the logger formatter for the emails."""
    return logging.Formatter(
        """
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        """,
        datefmt="%d/%m/%Y %H:%M:%S",
    )


def configure_logging(app):
    """Configure the loggers for the application."""
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]

    # Añadimos el logger por defecto a la lista de loggers
    loggers = [
        app.logger,
    ]
    handlers = []

    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    print(app.config)
    if (
        (app.config["APP_ENV"] == app.config["APP_ENV_LOCAL"])
        or (app.config["APP_ENV"] == app.config["APP_ENV_TESTING"])
        or (app.config["APP_ENV"] == app.config["APP_ENV_DEVELOPMENT"])
    ):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config["APP_ENV"] == app.config["APP_ENV_PRODUCTION"]:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler(
            (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            app.config["DONT_REPLY_FROM_EMAIL"],
            app.config["ADMINS"],
            "[Error][{}] La aplicación falló".format(app.config["APP_ENV"]),
            (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"]),
            (),
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


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


def create_app(settings_module="config.DevelopmentConfig"):
    """Create the application loading the config.

    Returns:
        app: the flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get("TESTING", False):
        app.config.from_pyfile("config-testing.py", silent=True)
    else:
        app.config.from_pyfile("config.py", silent=True)

    configure_logging(app)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    db.init_app(app)
    migrate.init_app(app, db)  # Se inicializa el objeto migrate

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

    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template("401.html"), 401
