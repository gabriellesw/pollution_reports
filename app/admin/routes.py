from flask import Blueprint

admin = Blueprint("admin", __name__)


@admin.route("/")
def admin_home():
    return "<h1>Admin Home</h1>"
