from flask import Blueprint

location_service = Blueprint("location_service", __name__, template_folder="templates")


@location_service.route("/")
def location_service_home():
    return "<h1>Location Service Home</h1>"
