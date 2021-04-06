from extensions import db
from config import Config
import datetime

CONFIG = Config()


class Complaint(db.Model):
    # Use to cross-reference more detailed complaint data sent to secure storage
    id = db.Column(db.Integer, primary_key=True)

    # Google Maps input fields
    polluter_search = db.Column(db.String)

    # Hidden fields populated by Google Maps via autocomplete.js
    polluter_lat = db.Column(db.String)
    polluter_lng = db.Column(db.String)
    polluter_street_number = db.Column(db.String)
    polluter_locality = db.Column(db.String)
    polluter_route = db.Column(db.String)
    polluter_administrative_area_level_1 = db.Column(db.String)
    polluter_administrative_area_level_2 = db.Column(db.String)
    polluter_postal_code = db.Column(db.String)
    polluter_name = db.Column(db.String)

    street_number = db.Column(db.String)
    route = db.Column(db.String)
    locality = db.Column(db.String)
    administrative_area_level_1 = db.Column(db.String)
    administrative_area_level_2 = db.Column(db.String)
    postal_code = db.Column(db.String)


    # Pre-populated by complaint_form.js
    date = db.Column(db.Date)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    ampm = db.Column(db.String)

    # Button Checkboxes handled by complaint_form.js
    ongoing = db.Column(db.Boolean)
    anonymous = db.Column(db.Boolean)

    # Fields that aren't set by JavaScript
    pollution_type = db.Column(db.String)
    description = db.Column(db.String)

    # Fields set after submission
    recorded_date = db.Column(db.DateTime)
    epa_confirmation_number = db.Column(db.String)

    def set_block(self, street_number):
        self.street_number = 100 * int(street_number / 100)