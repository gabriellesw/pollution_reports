from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config

CONFIG = Config()

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=CONFIG.DEFAULT_RATE_LIMITS.split(":")
)
