from extensions import db
from config import Config
import datetime

CONFIG = Config()


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
        polluter = self.polluter_name or "Polluter"
        sub = ""
        if self.submitted_to_calepa:
            sub = f"\nSubmitted to CalEPA on " \
                  f"{self.submitted_to_calepa_date:%b %d %Y, %I:%M %p} " \
                  f"\nCalEPA confirmation: {self.calepa_confirmation_number}"
        return f"""
        Complaint from {self.email} about {polluter} at {self.polluter_address}\n 
        {self.polluter_zip}, observed on {self.observed_date:%b %d %Y, %I:%M %p}{sub}
        """
