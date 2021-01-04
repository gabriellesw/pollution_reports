from flask import Flask


from .admin.routes import admin
from .api.routes import api
from .complaint_form.routes import complaint_form
from .location_service.routes import location_service
from .mapping.routes import mapping
from .site.routes import site

from extensions import *


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.FlaskConfig")

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(admin, url_prefix="/admin")
        app.register_blueprint(api, url_prefix="/api")
        app.register_blueprint(complaint_form, url_prefix="/complaint_form")
        app.register_blueprint(location_service, url_prefix="/location_service")
        app.register_blueprint(mapping, url_prefix="/mapping")
        app.register_blueprint(site)

    return app
