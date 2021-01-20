from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from extensions import db, login
from config import Config
import datetime

CONFIG = Config()


@login.user_loader
def get_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(CONFIG.varchar_max), nullable=False, unique=True)
    password = db.Column(db.String(CONFIG.varchar_max), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User-submitted fields collected from forms.ComplaintForm
    anonymous = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(CONFIG.varchar_max), nullable=False)
    confirm_email = db.Column(db.String(CONFIG.varchar_max), nullable=False)
    phone_number = db.Column(db.String(CONFIG.varchar_max))
    landline = db.Column(db.Boolean(), nullable=False)
    first_name = db.Column(db.String(CONFIG.varchar_max))
    last_name = db.Column(db.String(CONFIG.varchar_max))
    street = db.Column(db.String(CONFIG.varchar_max))
    city = db.Column(db.String(CONFIG.varchar_max))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(5))
    pollution_type = db.Column(db.Enum(*CONFIG.pollution_types), nullable=False)
    description = db.Column(db.Text(CONFIG.text_max), nullable=False)
    polluter_search = db.Column(db.String(CONFIG.varchar_max))
    polluter_street_number = db.Column(db.String(CONFIG.varchar_max), nullable=False)
    polluter_street_name = db.Column(db.String(CONFIG.varchar_max), nullable=False)
    polluter_city = db.Column(db.String(CONFIG.varchar_max), nullable=False)
    polluter_state = db.Column(db.String(2), nullable=False)
    polluter_zip = db.Column(db.String(5), nullable=False)
    observed_date = db.Column(db.DateTime(), nullable=False)
    ongoing = db.Column(db.Boolean(), nullable=False)
    consent_to_followup = db.Column(db.Boolean(), nullable=False)
    consent_to_campaign = db.Column(db.Boolean(), nullable=False)
    lat = db.Column(db.String(CONFIG.varchar_max))
    lng = db.Column(db.String(CONFIG.varchar_max))

    # Data updated by application
    submitted_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    submitted_to_calepa = db.Column(db.Boolean(), default=False)
    submitted_to_calepa_date = db.Column(db.DateTime())
    calepa_confirmation_number = db.Column(db.String(CONFIG.varchar_max))

    def __repr__(self):
        sub = ""
        if self.submitted_to_calepa:
            sub = f"\nSubmitted to CalEPA on " \
                  f"{self.submitted_to_calepa_date:%b %d %Y, %I:%M %p} " \
                  f"\nCalEPA confirmation: {self.calepa_confirmation_number}"
        return f"""
        Complaint from {self.email} about {self.polluter_search}\n 
        observed on {self.observed_date:%b %d %Y, %I:%M %p}{sub}
        """
