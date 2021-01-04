from flask import Blueprint, current_app

site = Blueprint("site", __name__)


@site.route("/")
def site_home():
    return "<h1>Site Home</h1>"
