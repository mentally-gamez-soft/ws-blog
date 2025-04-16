"""Create the flask application instance and config route."""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Declare a first test route.

    Returns:
        str: welcome message
    """
    return "Hello, World!"
