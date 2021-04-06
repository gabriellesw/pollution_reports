from flask import Flask, url_for
from config import Config

from .site.routes import site
from .models import *

from extensions import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    with app.app_context():
        app.register_blueprint(site)

    return app
