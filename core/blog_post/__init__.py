"""Declare the module for the blog posts and load the blueprint."""

from flask import Blueprint

blog_post_bp = Blueprint("blog_post", __name__, template_folder="templates")
from . import routes
