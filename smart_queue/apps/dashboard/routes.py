from flask import Blueprint, render_template

Dash = Blueprint("dash", __name__)


@Dash.route("/")
def index():
    return render_template("base.html")
