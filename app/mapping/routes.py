from flask import Blueprint, render_template

mapping = Blueprint("mapping", __name__, template_folder="templates")


@mapping.route("/")
def mapping_home():
    return render_template("mapping/mapping.html")
