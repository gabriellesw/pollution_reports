import requests
import gspread
import pathlib
import sys
from oauth2client.service_account import ServiceAccountCredentials
from lxml import html

from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from config import Config
from app.forms import ComplaintForm, format_minute
from app.models import Complaint, db

site = Blueprint("site", __name__, template_folder="templates")

CONFIG = Config()


def _send_to_epa(form):
    """
    Transmit pollution report to regulators. This particular implementation
    must parse the multi-page CalEPA web form (designed for humans), because there is no
    publicly-available API or service for submitting reports between organizations or
    agencies.

    We are basically relying on the fact that this organization is unlikely to have the
    resources to change their complaint form in the near future. This is the most
    fragile/breakable part of the process.

    :param form: WTForm
    :return: CalEPA confirmation number
    """
    if CONFIG.TESTING:
        return "#COMP-TEST1"

    #ToDo: This is currently not working at step 3
    else:
        local_form = form
        url = CONFIG.EPA_START_URL
        response = requests.get(url)
        tree = html.fromstring(response.content)

        # Grab state-preserving hidden fields & anything that's automatically posted
        form_data = {i.name: i.value for i in tree.xpath("//input[@type='hidden']")}
        form_data["Complaint:JCMC:theForm:j_id47"] = "Complaint:JCMC:theForm:j_id47"

        # Set complaint type as "air"
        air = tree.get_element_by_id("air")
        form_data[air.name] = air.xpath("@value")[0]

        # Post complaint type to start the process
        url = CONFIG.EPA_URL_1
        response = requests.post(url, form_data)
        tree = html.fromstring(response.content)

        # Grab hidden/default fields again from this new page
        form_data = {i.name: i.value for i in tree.xpath("//input[@type='hidden']")}
        form_data["details:JCMC:detailsForm:rAttach"] = ""
        form_data["details:JCMC:detailsForm:j_id107"] = "details:JCMC:detailsForm:j_id107"

        # Now we start filling in data from our local form
        if local_form.refinery.data:
            form_data["details:JCMC:detailsForm:j_id22"] = "on"
        form_data["details:JCMC:detailsForm:descriptionTextArea"] = local_form.description.data
        form_data["details:JCMC:detailsForm:previouslySubmittedTextArea"] = CONFIG.report_recipients
        form_data["details:JCMC:detailsForm:searchBox"] = local_form.polluter_search.data
        form_data["details:JCMC:detailsForm:address"] = f"{local_form.polluter_street_number.data}" \
                                                        f" {local_form.polluter_route.data}"
        form_data["details:JCMC:detailsForm:city"] = local_form.polluter_locality.data
        form_data["details:JCMC:detailsForm:county"] = local_form.polluter_administrative_area_level_2.data
        form_data["details:JCMC:detailsForm:state"] = local_form.polluter_administrative_area_level_1.data
        form_data["details:JCMC:detailsForm:zip"] = local_form.polluter_postal_code.data
        form_data["details:JCMC:detailsForm:latitude"] = local_form.polluter_lat.data
        form_data["details:JCMC:detailsForm:longitude"] = local_form.polluter_lng.data
        form_data["details:JCMC:detailsForm:geocoded"] = "true"

        # Our form is for stationary sources, where the RP should overlap with
        # the site of the violation. To make this clear, polluter info will
        # be repeated here.
        form_data["details:JCMC:detailsForm:locationDescriptionTextArea"] = ""
        form_data["details:JCMC:detailsForm:responsiblePartyNameInput"] = ""
        form_data["details:JCMC:detailsForm:responsiblePartyCompanyInput"] = local_form.polluter_name.data
        form_data["details:JCMC:detailsForm:rpStreet"] = f"{local_form.polluter_street_number.data}" \
                                                         f" {local_form.polluter_route.data}"
        form_data["details:JCMC:detailsForm:rpCity"] = local_form.polluter_locality.data
        form_data["details:JCMC:detailsForm:rpState"] = local_form.polluter_administrative_area_level_1.data
        form_data["details:JCMC:detailsForm:rpZip"] = local_form.polluter_postal_code.data

        form_data["details:JCMC:detailsForm:airVehicle"] = "Stationary Source"
        form_data["details:JCMC:detailsForm:airsource"] = local_form.pollution_type.data
        form_data["details:JCMC:detailsForm:occuranceTimeFrame"] = "Exact Date"
        form_data["details:JCMC:detailsForm:dateOfOccurence"] = f"{local_form.observed_date.data.strftime('%m/%d/%Y')}" \
                                                                f"{local_form.hour.data}:" \
                                                                f"{format_minute(local_form.minute.data)}" \
                                                                f" {local_form.ampm.data}"
        if local_form.ongoing.data:
            form_data["details:JCMC:detailsForm:ongoingOccurance"] = "on"

        # Post complaint details and move to contact page
        url = CONFIG.EPA_URL_2
        response = requests.post(url, form_data)
        tree = html.fromstring(response.content)

        # Add values of hidden/default fields to final POST request
        form_data = {i.name: i.value for i in tree.xpath("//input[@type='hidden']")}
        form_data["ComplaintContact:JCMC:AnonymousForm"] = "ComplaintContact:JCMC:AnonymousForm"
        form_data["ComplaintContact:JCMC:AnonymousForm:refH"] = "false"
        form_data["ComplaintContact:JCMC:AnonymousForm:ReferringAgency"] = ""
        form_data["ComplaintContact:JCMC:AnonymousForm:ReferringName"] = ""
        form_data["ComplaintContact:JCMC:AnonymousForm:referalEmail"] = ""

        if local_form.anonymous.data:
            form_data["ComplaintContact:JCMC:AnonymousForm:anonH"] = "true"
            form_data["ComplaintContact:JCMC:AnonymousForm:FirstName"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:LastName"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingStreet"] = f""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingCity"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingState"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingPostalCode"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonHomePhone"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMobilePhone"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:email"] = ""
            form_data["ComplaintContact:JCMC:AnonymousForm:confirmEmail"] = ""


        else:
            form_data["ComplaintContact:JCMC:AnonymousForm:anonH"] = "false"
            if not local_form.first_name.data:
                form_data["ComplaintContact:JCMC:AnonymousForm:FirstName"] = "Declined"
            else:
                form_data["ComplaintContact:JCMC:AnonymousForm:FirstName"] = local_form.first_name.data
            if not local_form.last_name.data:
                form_data["ComplaintContact:JCMC:AnonymousForm:LastName"] = "Declined"
            else:
                form_data["ComplaintContact:JCMC:AnonymousForm:LastName"] = local_form.last_name.data

            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingStreet"] = f"{local_form.street_number.data} " \
                                                                                   f" {local_form.route.data}"
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingCity"] = local_form.locality.data
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingState"] = local_form.administrative_area_level_1.data
            form_data["ComplaintContact:JCMC:AnonymousForm:PersonMailingPostalCode"] = local_form.postal_code.data
            if local_form.landline.data:
                form_data["ComplaintContact:JCMC:AnonymousForm:PersonHomePhone"] = local_form.phone.data
                form_data["ComplaintContact:JCMC:AnonymousForm:PersonMobilePhone"] = ""
            else:
                form_data["ComplaintContact:JCMC:AnonymousForm:PersonHomePhone"] = ""
                form_data["ComplaintContact:JCMC:AnonymousForm:PersonMobilePhone"] = local_form.phone.data

            form_data["ComplaintContact:JCMC:AnonymousForm:email"] = local_form.email.data
            form_data["ComplaintContact:JCMC:AnonymousForm:confirmEmail"] = local_form.confirm_email.data

        form_data["ComplaintContact:JCMC:AnonymousForm:emailOptOut"] = "on" # This is the opposite of what you think it is
        form_data["ComplaintContact:JCMC:AnonymousForm:j_id88"] = "ComplaintContact:JCMC:AnonymousForm:j_id88"

        # Final post to get complaint number
        url = CONFIG.EPA_URL_3
        response = requests.post(url, form_data)
        tree = html.fromstring(response.content)

        complaint_number = tree.get_element_by_id("complaintNumber")  #????
        complaint_number = tree.xpath("//span[@id='complaintNumber']/text()")[0]
        return complaint_number


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
    complaint = Complaint(**data)
    complaint.set_block()
    complaint.epa_confirmation_number = epa_conf
    db.session.add(complaint)
    db.session.commit()
    return complaint


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
    :param model: SQLAlchemy Model
    :return: EPA Confirmation Number
    """
    confirmation_no = _send_to_epa(form)
    complaint = _save_local(form, confirmation_no)
    _send_to_sheets(form, complaint)
    return confirmation_no


@site.route("/", methods=["GET", "POST"])
def home():
    form = ComplaintForm()
    if form.validate_on_submit():
        # return redirect(url_for("site.home"))
        conf_no = process_form(form)
        return f"{conf_no}\n{form.data}"
    elif form.is_submitted():
        errors = []
        for field in form:
            for error in form[field.name].errors:
                errors.append(f"{field.name}: {error}")
        errors = "\n".join(errors)
        return f"{errors}\n\n\n{form.data}"
    return render_template(
        "site/main.html",
        form=form,
        places_api_key=CONFIG.PLACES_API_KEY,
        recaptcha_public_key=CONFIG.RECAPTCHA_PUBLIC_KEY,
    )


@site.route('/favicon.ico')
def favicon():
    return redirect(url_for("static", filename="icons/favicon.ico"))
