from extensions import db
from config import Config
import datetime

CONFIG = Config()


class Complaint(db.Model):
    # Use to cross-reference more detailed complaint data sent to secure storage
    id = db.Column(db.Integer, primary_key=True)

    # Complainant info
    lat = db.Column(db.String(CONFIG.varchar_max))
    lng = db.Column(db.String(CONFIG.varchar_max))
    observed_date = db.Column(db.String(CONFIG.varchar_max))

    # Polluter info
    pollution_type = db.Column(db.Enum(*CONFIG.pollution_types), nullable=False)
    description = db.Column(db.Text(CONFIG.text_max), nullable=False)
    polluter_place_id = db.Column(db.String(CONFIG.varchar_max))  # Google placeID
    polluter_lat = db.Column(db.String(CONFIG.varchar_max))
    polluter_lng = db.Column(db.String(CONFIG.varchar_max))

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
