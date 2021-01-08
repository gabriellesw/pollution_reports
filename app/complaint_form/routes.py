from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import ComplaintForm

complaint_form = Blueprint("complaint_form", __name__, template_folder="templates")


@complaint_form.route("/", methods=["GET", "POST"])
def complaint_form_home():
    form = ComplaintForm()
    form_about = """Use this form to notify us about local polluters
    in your area. Your complaint will be used as part of
    our ongoing investigations. It will also be forwarded
    to state and local regulators. You may be contacted by
    a local investigator about your complaint."""
    if form.validate_on_submit():
        flash("Thank you for submitting your complaint")
        return redirect(url_for("site.site_home"))
    return render_template(
        "complaint_form/complaint.html",
        form=form, form_about=form_about,
        title="Test Complaints"
    )
