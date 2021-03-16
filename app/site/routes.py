from flask import Blueprint, render_template

site = Blueprint("site", __name__, template_folder="templates")


@site.route("/")
def home():
    return render_template("site/template.html")

@site.route("/about")
def about():
    return "about"

@site.route("/privacy")
def privacy():
    return "privacy"