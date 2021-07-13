from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
csrf = CSRFProtect()
