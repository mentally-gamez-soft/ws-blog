"""Create the flask application instance and config route."""

from flask import Flask, redirect, render_template, request, url_for

from core.blog_post.forms import BlogPostForm
from core.users.forms import SignupForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec

posts = []


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

        next = request.args.get("next", None)
        if next:
            return redirect(next)
        return redirect(url_for("index"))

    return render_template("users/signup_form.html", form=form)
