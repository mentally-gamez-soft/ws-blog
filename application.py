"""Create the flask application instance and config route."""

from flask import Flask, render_template

app = Flask(__name__)

posts = []


@app.route("/")
def index():
    """Declare the index route.

    Returns:
        str: the number of existing posts.
    """
    return render_template("index.html", num_posts=len(posts))


@app.route("/post/<string:slug>/")
def show_post(slug):
    """Show a post by its slug.

    Args:
        slug (str): The title of the post as slug.

    Returns:
        str: The post title.
    """
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    """Define the form to consult a post and to modify it.

    Args:
        post_id (int, optional): The id of the post. Defaults to None.

    Returns:
        str: Indicate the id of the post.
    """
    return render_template("admin/post_form.html", post_id=post_id)
