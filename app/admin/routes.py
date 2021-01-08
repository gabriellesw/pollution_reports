from flask import Blueprint, render_template, url_for

admin = Blueprint("admin", __name__, template_folder="templates")

COMPLAINTS = [
    {"id": "0", "date": "2020-12-12", "name": "John Smith", "lat": 34.5433, "long": -122.38484},
    {"id": "1", "date": "2020-12-01", "name": "M. Law", "lat": 34.93838, "long": -122.354633},
    {"id": "2", "date": "2020-11-24", "name": "John Smith", "lat": 34.45843, "long": -122.2833772}
]


@admin.route("/")
def admin_home():
    user = {"username": "Gabrielle"}

    return render_template(
        "admin/admin.html",
        title="Pollution Complaints",
        user=user,
        complaints=COMPLAINTS,
    )


@admin.route("/complaint/<int:complaint_id>")
def view_complaint(complaint_id):
    complaint = COMPLAINTS[complaint_id]
    return render_template("admin/complaint.html", complaint=complaint)
