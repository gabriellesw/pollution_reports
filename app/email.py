from flask import render_template
from sendgrid import SendGridAPIClient, SendGridException
from sendgrid.helpers.mail import Mail
from config import Config

CONFIG = Config()


def confirm_complaint(
        to_email,
        complaint,
        from_email=CONFIG.SENDGRID_COMPLAINT_FROM,
        subject=CONFIG.COMPLAINT_SUBJECT,
):
    """
    :param to_email:
    :param complaint: Complaint Model
    :param from_email:
    :param subject:
    :return:
    """

    message = Mail(
        from_email=from_email,
        to_emails=[to_email],
        subject=subject,
        html_content=render_template("email/confirm_complaint.html", complaint=complaint)
    )

    try:
        sender = SendGridAPIClient(CONFIG.SENDGRID_API_KEY)
        response = sender.send(message)
        if response.status_code != 250:
            raise SendGridException(
                f"Code: {response.status_code}\n"
                f"Message: {response.headers}\n"
                f"{response.body}"
            )
    except:
        raise