from flask import Blueprint, render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from flask_security import current_user, hash_password, auth_required, roles_required
from app.models import *
# from app.forms import LoginForm, NewUserForm
from config import Config

from extensions import *

CONFIG = Config()

dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.before_app_first_request
def get_or_create_admin_user():
    db.create_all()
    if not datastore.find_user(email=CONFIG.DEFAULT_USER_EMAIL):
        datastore.find_or_create_role(name=CONFIG.admin_role)
        datastore.find_or_create_role(name=CONFIG.readonly_role)
        admin_role = Role.query.filter_by(name=CONFIG.admin_role).first()
        datastore.create_user(
            email=CONFIG.DEFAULT_USER_EMAIL,
            password=hash_password(CONFIG.DEFAULT_USER_PASSWORD)
        )
        admin_user = datastore.find_user(email=CONFIG.DEFAULT_USER_EMAIL)
        datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()


@dashboard.route("/")
@auth_required()
def dashboard_home():
    user = current_user
    # ToDo: Add pagination
    complaints = Complaint.query.order_by(Complaint.observed_date.desc()).limit(10).all()

    summary_columns = [
        "observed_date",
        "polluter_search",
    ]

    return render_template(
        "dashboard/dashboard.html",
        title="Pollution Complaints",
        user=user,
        complaints=complaints,
        headers=summary_columns,
    )


@dashboard.route("/complaint/<int:complaint_id>")
def view_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    return render_template("dashboard/complaint.html", complaint=complaint)


@dashboard.route("/control_panel")
@roles_required(CONFIG.admin_role)
def control_panel():
    return "it worked"
    # form = NewUserForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash("Unable to log in")
    #         return redirect(url_for("dashboard.login"))
    #     login_user(user, remember=form.remember.data)
    #     next = request.args.get("next")
    #     if not next or url_parse(next).netloc != "":
    #         next = url_for("dashboard.dashboard")
    #     return redirect(next)
    # return render_template("dashboard/login.html", form=form)