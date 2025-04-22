"""Declare the entry point for the flask application."""

import os

from flask import send_from_directory

from core import create_app

settings_module = os.getenv("APP_SETTINGS_MODULE")
print("settings_module = {}".format(settings_module))
app = create_app(settings_module)


@app.route("/media/posts/<filename>")
def media_posts(filename):
    """Define the route to the static files for the dev and local servers.

    Args:
        filename (str): the name of an image file.

    Returns:
        Response: the response for the stored file.
    """
    dir_path = os.path.join(
        app.config["MEDIA_DIR"], app.config["POSTS_IMAGES_DIR"]
    )
    return send_from_directory(dir_path, filename)
