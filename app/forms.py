from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, TextAreaField, SelectField, DateTimeField, HiddenField
)
from wtforms.validators import Optional

from app.custom_validators import (InputRequired, LengthNA, InputRequiredNA, EmailNA, ConfirmEmail, Phone,
                                   Length)
from config import Config

CONFIG = Config()


def format_minute(minute):
    if minute < 10:
        return f"0{minute}"
    return str(minute)


class ComplaintForm(FlaskForm):
    # Google Maps input fields
    polluter_search = StringField(validators=[InputRequired("You must include a pollution source")])
    reporter_search = StringField(validators=[LengthNA(max=CONFIG.varchar_max), Optional()])

    # Hidden fields populated by Google Maps via autocomplete.js
    polluter_lat = HiddenField()
    polluter_lng = HiddenField()
    polluter_street_number = HiddenField()
    polluter_locality = HiddenField()
    polluter_route = HiddenField()
    polluter_address = HiddenField()
    polluter_administrative_area_level_1 = HiddenField()
    polluter_administrative_area_level_2 = HiddenField()
    polluter_postal_code = HiddenField()
    polluter_name = HiddenField()

    lat = HiddenField()
    lng = HiddenField()
    street_number = HiddenField()
    locality = HiddenField()
    route = HiddenField()
    address = HiddenField()
    administrative_area_level_1 = HiddenField()
    administrative_area_level_2 = HiddenField()
    postal_code = HiddenField()

    # Pre-populated by complaint_form.js
    date = DateTimeField(format=CONFIG.date_format, validators=[InputRequired("You must include a date")])
    hour = SelectField(choices=range(1, 13))
    minute = SelectField(choices=list(zip(range(60), map(format_minute, range(60)))))
    ampm = SelectField(choices=["AM", "PM"])
    full_date = HiddenField()

    # Button Checkboxes handled by complaint_form.js
    ongoing = BooleanField()
    refinery = BooleanField()
    anonymous = BooleanField()
    landline = BooleanField()
    privacy_contact_ok = BooleanField(default="checked")

    # Fields that aren't set by JavaScript
    pollution_type = SelectField(choices=CONFIG.pollution_types)
    description = TextAreaField(validators=[InputRequired("A description of the pollution is required"), Length(max=CONFIG.text_max)])
    email = StringField(validators=[InputRequiredNA(), EmailNA()])
    confirm_email = StringField(validators=[InputRequiredNA(), ConfirmEmail()])
    phone = StringField(validators=[Optional(), Phone()])
    first_name = StringField(validators=[InputRequiredNA(), LengthNA(max=CONFIG.varchar_max)])
    last_name = StringField(validators=[InputRequiredNA(), LengthNA(max=CONFIG.varchar_max)])
