from flask import Blueprint, render_template, request
from config import Config
from app.forms import ComplaintForm

site = Blueprint("site", __name__, template_folder="templates")

CONFIG = Config()


@site.route("/", methods=["GET", "POST"])
def home():
    form = ComplaintForm()
    return render_template(
        "site/template.html",
        form=form,
        places_api_key=CONFIG.PLACES_API_KEY,
        recaptcha_public_key=CONFIG.RECAPTCHA_PUBLIC_KEY,
    )
