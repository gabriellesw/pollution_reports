import requests
import gspread
import pathlib

from oauth2client.service_account import ServiceAccountCredentials

from flask import Blueprint, render_template, request, redirect, url_for
from config import Config
from app.forms import ComplaintForm, format_minute
from app.models import Complaint, db
from app.third_party_form import ThirdPartyReport
site = Blueprint("site", __name__, template_folder="templates")

CONFIG = Config()


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
        return "COMP-TEST"
    third_party_form = ThirdPartyReport(form)
    confirmation_no = third_party_form.get_response()
    return confirmation_no


def _send_to_sheets(form, model):
    """
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
@site.route("/<conf_no>", methods=["GET", "POST"])
def home(conf_no=None):
    form = ComplaintForm()
    if form.validate_on_submit():
        conf_no = process_form(form)
        return redirect(url_for("site.home", conf_no=conf_no))
    return render_template(
        "site/main.html",
        form=form,
        epa_confirmation_no=conf_no,
        places_api_key=CONFIG.PLACES_API_KEY,
        recaptcha_public_key=CONFIG.RECAPTCHA_PUBLIC_KEY,
    )


@site.route('/favicon.ico')
def favicon():
    return redirect(url_for("static", filename="icons/favicon.ico"))
