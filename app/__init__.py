from flask import Flask
from config import Config

from .complaint_form.routes import complaint_form
from .location_service.routes import location_service
from .mapping.routes import mapping
from .site.routes import site
from .models import *

from extensions import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.register_blueprint(complaint_form, url_prefix="/complaint_form")
        app.register_blueprint(location_service, url_prefix="/location_service")
        app.register_blueprint(mapping, url_prefix="/mapping")
        app.register_blueprint(site)

    return app
