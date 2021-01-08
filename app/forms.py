from flask_wtf import FlaskForm
from wtforms import (
    StringField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeField
)
from wtforms.validators import Email, InputRequired, Length, Optional
from app.custom_validators import Zip, Phone, ConfirmEmail
import datetime


class ComplaintForm(FlaskForm):
    email = StringField("Email Address", validators=[Email(), InputRequired()])
    confirm_email = StringField("Confirm Email", validators=[
        Email(), ConfirmEmail(), InputRequired()
    ])
    phone_number = StringField("Phone", validators=[Optional(), Phone()])
    landline = BooleanField("My Phone is a Land Line")

    first_name = StringField("First Name", validators=[Optional(), Length(-1, 500)])
    last_name = StringField("Last Name", validators=[Optional(), Length(-1, 500)])

    street = StringField("Street Address", validators=[Optional()])
    city = StringField("City", validators=[Optional()])
    state = StringField("State", validators=[Optional()])
    zip = StringField("ZIP Code", validators=[Optional(), Zip()])
    type = SelectField("What kind of pollution is it? If you can smell the pollution, "
                       "choose 'Odors'. Otherwise, choose the option that best "
                       "describes what you're seeing",
                       validators=[InputRequired()],
                       choices=["Odors", "Smoke", "Asbestos", "Dust"]
                       )
    description = TextAreaField("Describe the pollution you've witnessed in your own "
                                "words. Odors, visible smoke or dust, sounds, "
                                "and any other activity that might help investigators",
                                validators=[InputRequired(), Length(-1, 10000)])
    polluter_search = StringField("Address, Intersection or Name of Corporation "
                                  "emitting the pollution",
                                  validators=[InputRequired(), Length(-1, 500)])

    date = DateTimeField(
        "When did you most recently witness the pollution?",
        validators=[InputRequired()],
        format="%b %d %Y, %-I:%M %p",
        default=datetime.datetime.utcnow()
    )
    ongoing = BooleanField("Is this a regular/ongoing occurrence?")

    consent_to_followup = BooleanField("I understand that a local investigator may "
                                       "contact me about my complaint", default=1)
    consent_to_campaign = BooleanField("I agree to be contacted about this and other "
                                       "campaigns to stop air pollution", default=1)
    anonymous = BooleanField("I wish to submit my complaint anonymously")

    send_complaint = SubmitField("Send my complaint now!")


