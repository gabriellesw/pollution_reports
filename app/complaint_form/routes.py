from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import ComplaintForm
from app.models import Complaint
from extensions import db
import datetime

complaint_form = Blueprint("complaint_form", __name__, template_folder="templates")
from config import Config

CONFIG = Config()


@complaint_form.context_processor
def current_timestamp():
    return {"current_timestamp": datetime.datetime.utcnow().strftime(CONFIG.date_format)}


@complaint_form.route("/", methods=["GET", "POST"])
def complaint_form_home():
    form = ComplaintForm()
    form_about = """Use this form to notify us about local polluters
    in your area. Your complaint will be used as part of
    our ongoing investigations. It will also be forwarded
    to state and local regulators. You may be contacted by
    a local investigator about your complaint."""
    if form.validate_on_submit():
        fields = {field.name: field.data for field in form}
        fields.pop("send_complaint")  # Remove submit button
        fields.pop("csrf_token")  # Remove hidden fields
        complaint = Complaint(**fields)
        db.session.add(complaint)
        db.session.commit()
        flash("Thank you for submitting your complaint")
        return redirect(url_for("site.site_home"))
    return render_template(
        "complaint_form/complaint.html",
        form=form, form_about=form_about,
        title="Test Complaints"
    )
