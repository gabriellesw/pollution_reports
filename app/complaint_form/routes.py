from flask import Blueprint

complaint_form = Blueprint("complaint_form", __name__)


@complaint_form.route("/")
def complaint_form_home():
    return "<h1>Complaint Form Home</h1>"
