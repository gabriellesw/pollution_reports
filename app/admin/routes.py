from flask import Blueprint, render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Complaint
from app.forms import LoginForm


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Unable to log in")
            return redirect(url_for("admin.login"))
        login_user(user, remember=form.remember.data)
        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("admin.admin_home")
        return redirect(next)
    return render_template("admin/login.html", form=form)


@admin.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin.route("/")
@login_required
def admin_home():
    user = current_user
    # ToDo: Add pagination
    complaints = Complaint.query.order_by(Complaint.observed_date.desc()).limit(10).all()

    summary_columns = [
        "observed_date",
        "polluter_search",
    ]

    return render_template(
        "admin/admin.html",
        title="Pollution Complaints",
        user=user,
        complaints=complaints,
        headers=summary_columns,
    )


@admin.route("/complaint/<int:complaint_id>")
def view_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    return render_template("admin/complaint.html", complaint=complaint)
