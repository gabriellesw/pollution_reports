from flask import Blueprint, render_template
from config import Config

site = Blueprint("site", __name__, template_folder="templates")

CONFIG = Config()


@site.route("/")
def home():
    return render_template(
        "site/template.html",
        places_api_key=CONFIG.PLACES_API_KEY,
    )


@site.route("/about")
def about():
    return "about"


@site.route("/privacy")
def privacy():
    return "privacy"
