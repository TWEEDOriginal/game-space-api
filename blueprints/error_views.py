from flask import Blueprint, redirect, render_template

miscellanous = Blueprint("miscellanous", __name__)


@miscellanous.route("/")
def index():
    """
    refers base url to /docs
    """
    return redirect("/docs")


@miscellanous.app_errorhandler(404)
def not_found(e):
    """
    Error handling for pages that do not exist
    """
    return render_template("404.html"), 404
