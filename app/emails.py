from flask import render_template
from sendgrid import SendGridAPIClient, SendGridException
from sendgrid.helpers.mail import Mail, To

from config import Config

CONFIG = Config()


def _send_mail(message):
        client = SendGridAPIClient(CONFIG.SENDGRID_API_KEY)
        response = client.send(message)
        if response.status_code >= 300:
            sg_url = "https://sendgrid.com/docs/for-developers/sending-email/" \
                       "smtp-errors-and-troubleshooting/"
            wk_url = "https://en.wikipedia.org/wiki/List_of_SMTP_server_return_codes"
            raise SendGridException(f"Message failed or delayed: status code: "
                                    f"{response.status_code}. See {sg_url} and"
                                    f" {wk_url}")


def send_complaint_confirmation(form, conf_no):
    """
    Send a copy of complaint to user
    :param form: WTForm
    :param conf_no: String
    """
    message = Mail(
        from_email=CONFIG.SENDGRID_FROM,
        to_emails=To(form.email.data),
        subject="Your Pollution Complaint",
        plain_text_content=render_template("email/complaint_confirmation.txt", form=form, conf_no=conf_no),
        html_content=render_template("email/complaint_confirmation.html", form=form, conf_no=conf_no),
    )
    _send_mail(message)
