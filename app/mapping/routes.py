from flask import Blueprint

mapping = Blueprint("mapping", __name__)


@mapping.route("/")
def mapping_home():
    return "<h1>Mapping Home</h1>"
