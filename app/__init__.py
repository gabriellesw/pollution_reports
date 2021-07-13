from flask import Flask

from config import Config
from extensions import db, migrate, moment, csrf, limiter
from .site.routes import site


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        app.register_blueprint(site)

    return app
