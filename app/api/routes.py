from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/")
def api_home():
    return "<h1>API Home</h1>"
