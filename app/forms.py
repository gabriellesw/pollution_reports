from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField,
    HiddenField, PasswordField
)
from wtforms.validators import Email, InputRequired, Length, Optional
from app.custom_validators import Zip, Phone, ConfirmEmail

from config import Config

CONFIG = Config()


def format_minute(minute):
    if minute < 10:
        return f"0{minute}"
    return str(minute)


class ComplaintForm(FlaskForm):
    # Google Maps input fields
    polluter_search = StringField()
    reporter_search = StringField()

    # Hidden fields populated by Google Maps via autocomplete.js
    polluter_lat = HiddenField()
    polluter_lng = HiddenField()
    polluter_street_number = HiddenField()
    polluter_locality = HiddenField()
    polluter_route = HiddenField()
    polluter_administrative_area_level_1 = HiddenField()
    polluter_postal_code = HiddenField()

    lat = HiddenField()
    lng = HiddenField()
    street_number = HiddenField()
    locality = HiddenField()
    route = HiddenField()
    administrative_area_level_1 = HiddenField()
    postal_code = HiddenField()

    # Pre-populated by complaint_form.js
    date = DateTimeField(format=CONFIG.date_format)
    hour = SelectField(choices=range(1, 13))
    minute = SelectField(choices=list(zip(range(60), map(format_minute, range(60)))))
    ampm = SelectField(choices=[("am", "AM"), ("pm", "PM")])

    # Button Checkboxes handled by complaint_form.js
    ongoing = BooleanField()
    anonymous = BooleanField()
    landline = BooleanField()
    privacy_contact_ok = BooleanField(default="checked")

    # Fields that aren't set by JavaScript
    pollution_type = SelectField(choices=CONFIG.pollution_types)
    description = TextAreaField()
    email = StringField()
    confirm_email = StringField()
    phone = StringField()
    first_name = StringField()
    last_name = StringField()

