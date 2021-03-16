from flask import Blueprint, render_template

site = Blueprint("site", __name__, template_folder="templates")


@site.route("/")
def site_home():
    return render_template("site/template.html")
