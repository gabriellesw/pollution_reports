import json
import pathlib

import gspread
import requests
from flask import Blueprint, render_template, redirect, url_for, current_app, request
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.exceptions import TooManyRequests

from app.emails import send_complaint_confirmation
from app.forms import ComplaintForm
from app.models import Complaint, db
from app.third_party_form import ThirdPartyReport
from config import Config
from extensions import limiter

site = Blueprint("site", __name__, template_folder="templates")

CONFIG = Config()


def check_captcha(response):
    secret = CONFIG.RECAPTCHA_SECRET_KEY
    url = "https://www.google.com/recaptcha/api/siteverify"
    api_response = requests.post(url, {"secret": secret, "response": response})
    if json.loads(api_response.content).get("success") != True:
        raise ConnectionRefusedError(str(api_response.content) + "\n" + response)


def _save_local(form, epa_conf):
    """
    Save anonymized local copy of complaint
    :param form: WTForm
    :param epa_conf: String
    :return: complaint ID
    """
    data = form.data.copy()
    data.pop("csrf_token")
    data.pop("reporter_search")
    data.pop("lat")
    data.pop("lng")
    data.pop("first_name")
    data.pop("last_name")
    data.pop("email")
    data.pop("confirm_email")
    data.pop("phone")
    data.pop("landline")
    data.pop("privacy_contact_ok")
    data.pop("address")
    data.pop("full_date")
    data.pop("polluter_address")
    complaint = Complaint(**data)
    complaint.set_block()
    complaint.epa_confirmation_number = epa_conf
    db.session.add(complaint)
    db.session.commit()
    return complaint


def _send_to_third_party(form):
    if CONFIG.DEBUG:
        return "#COMP-TEST1"
    third_party_form = ThirdPartyReport(form)
    confirmation_no = third_party_form.get_response()
    return confirmation_no


def _send_to_sheets(form, model):
    """
    # ToDo: move this to a new home
    Send detailed, combined report data to Google sheet
    :param form: WTForm
    :param model: db.Model
    :return: None
    """
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        pathlib.Path(__file__).parents[2].joinpath("keys.json"),
        scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open(CONFIG.GSHEET).sheet1

    gsheet_data = []

    for k in CONFIG.GSHEET_COLS:
        data = str(form.data[k])
        gsheet_data.append(data)

    gsheet_data.append(str(model.recorded_date))
    gsheet_data.append(model.epa_confirmation_number)

    if not sheet.get("A1"):
        gsheet_headers = []
        for k in CONFIG.GSHEET_COLS:
            gsheet_headers.append(k)

        gsheet_headers.append("recorded_date")
        gsheet_headers.append("epa_confirmation_number")
        sheet.append_row(gsheet_headers)

    sheet.append_row(gsheet_data)


def process_form(form):
    """
    Send data to EPA, Google Sheets, and local database
    :param form: WTForm
    :return: EPA Confirmation Number
    """
    confirmation_no = _send_to_third_party(form)
    complaint = _save_local(form, confirmation_no)
    _send_to_sheets(form, complaint)
    return confirmation_no


@site.route("/", methods=["GET", "POST"])
@limiter.limit(limit_value=CONFIG.POST_RATE_LIMIT, methods=["POST"])
def home():
    form = ComplaintForm()
    if form.validate_on_submit():
        check_captcha(request.form["g-recaptcha-response"])
        conf_no = process_form(form)
        if not form.anonymous.data:
            send_complaint_confirmation(form, conf_no)
        return redirect(url_for("site.home", conf_no=conf_no))
    return render_template(
        "site/main.html",
        form=form,
        epa_confirmation_no=request.args.get("conf_no"),
        error=request.args.get("error"),
        places_api_key=CONFIG.PLACES_API_KEY,
        recaptcha_public_key=CONFIG.RECAPTCHA_PUBLIC_KEY,
    )


@site.route('/favicon.ico')
def favicon():
    return redirect(url_for("static", filename="icons/favicon.ico"))


@site.app_errorhandler(Exception)
def any_error(error):
    """
    Log the full stack trace privately and display a vague error message to user
    """
    current_app.logger.error(error, exc_info=True)
    code = getattr(error, "code", 404)
    if code == 429 and request.method == "GET":
        # Do not redirect when rate limit exceeded on get requests.
        # This will cause endless redirects
        raise TooManyRequests()
    return redirect(url_for("site.home", error=404))
