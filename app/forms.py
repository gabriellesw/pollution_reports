from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField
)
from wtforms.validators import Email, InputRequired, Length, Optional
from app.custom_validators import Zip, Phone, ConfirmEmail

from config import Config

CONFIG = Config()


class ComplaintForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[Email(), InputRequired(), Length(max=CONFIG.varchar_max)]
    )
    confirm_email = StringField("Confirm Email", validators=[
        Email(), ConfirmEmail(), InputRequired()
    ])
    phone_number = StringField("Phone", validators=[Optional(), Phone()])
    landline = BooleanField("My Phone is a Land Line")

    first_name = StringField(
        "First Name",
        validators=[Optional(), Length(max=CONFIG.varchar_max)]
    )
    last_name = StringField(
        "Last Name",
        validators=[Optional(), Length(max=CONFIG.varchar_max)]
    )

    street = StringField(
        "Street Address",
        validators=[Optional(), Length(max=CONFIG.varchar_max)]
    )
    city = StringField(
        "City",
        validators=[Optional(), Length(max=CONFIG.varchar_max)]
    )
    state = StringField("State", validators=[Optional(), Length(max=2)])
    zip = StringField("ZIP Code", validators=[Optional(), Zip(), Length(max=5)])
    type = SelectField("Primary Concern",
                       validators=[InputRequired()],
                       choices=CONFIG.pollution_types
                       )
    description = TextAreaField(
        "Describe the pollution you've witnessed in your own words. Odors, visible "
        "smoke or dust, sounds, and any other activity that you think will help "
        "investigators research and act upon your complaint.",
        validators=[InputRequired(), Length(-1, CONFIG.text_max)]
    )

    polluter_search_field = StringField(
        "Address, Intersection or Name of Corporation emitting the pollution",
        validators=[Length(max=CONFIG.varchar_max)],
        id="polluter_search",
        render_kw={"onFocus": "geolocate()"},
    )

    polluter_street_number = StringField(
        "Street Number",
        validators=[Length(max=CONFIG.varchar_max)],
        id="street_number",
        render_kw={"disabled": "true"}
    )

    polluter_street_name = StringField(
        "Street Name",
        validators=[Length(max=CONFIG.varchar_max)],
        id="route",
        render_kw={"disabled": "true"}
    )

    polluter_city = StringField(
        "City",
        validators=[Length(max=CONFIG.varchar_max)],
        id="locality",
        render_kw={"disabled": "true"}
    )
    polluter_state = StringField(
        "State",
        validators=[Length(max=2)],
        id="administrative_area_level_1",
        render_kw={"disabled": "true"}
    )
    polluter_zip = StringField(
        "Zip",
        validators=[Length(max=5)],
        id="postal_code",
        render_kw={"disabled": "true"}
    )

    observed_date = DateTimeField(
        "When did you most recently witness the pollution?",
        validators=[InputRequired()],
        format=CONFIG.date_format,
    )
    ongoing = BooleanField("Is this a regular/ongoing occurrence?")

    consent_to_followup = BooleanField(
        "I understand that a local investigator may contact me about my complaint",
        default=1
    )
    consent_to_campaign = BooleanField(
        "I agree to be contacted about this and other campaigns to stop air pollution",
        default=1
    )
    anonymous = BooleanField("I wish to submit my complaint anonymously")

    send_complaint = SubmitField("Send my complaint now!")


