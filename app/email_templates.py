from flask import render_template
from sendgrid import SendGridAPIClient, SendGridException
from sendgrid.helpers.mail import Mail
from config import Config

CONFIG = Config()


def send_transactional_email(
        to_email,
        from_email,
        subject,
        template_path,
        **template_kwargs,
):
    """
    Use Sendgrid to communicate with organizers and reporters
    :param to_email: recipient
    :param from_email: "from" address must match approved Sendgrid ID
    :param subject: template-specific subject
    :param template_path: relative path to Jinja2 template
    :param template_kwargs: Additional kwargs for template
        template
    """
    message = Mail(
        from_email=from_email,
        to_emails=[to_email],
        subject=subject,
        html_content=render_template(template_path, **template_kwargs)
    )
    sender = SendGridAPIClient(CONFIG.SENDGRID_API_KEY)
    response = sender.send(message)
    if response.status_code != 250:
        raise SendGridException(
            f"Code: {response.status_code}\n"
            f"Message: {response.headers}\n"
            f"{response.body}"
            )


def confirm_password_reset(
    to_email,
    organizer,
):
    send_transactional_email(
        to_email,
        from_email=CONFIG.SENDGRID_ORGANIZER_FROM,
        subject=CONFIG.RESET_SUCCESS_SUBJECT,
        template_path="email/confirm_password_reset.html",
        organizer=organizer
    )


def reset_password(
        to_email,
        organizer,
):
    send_transactional_email(
        to_email,
        from_email=CONFIG.SENDGRID_ORGANIZER_FROM,
        subject=CONFIG.RESET_PASSWORD_SUBJECT,
        template_path="email/reset_password.html",
        organizer=organizer,
    )


def welcome_organizer(
        to_email,
        organizer,

):
    send_transactional_email(
        to_email,
        from_email=CONFIG.SENDGRID_ORGANIZER_FROM,
        subject=CONFIG.WELCOME_SUBJECT,
        template_path="email/welcome_organizer.html",
        organizer=organizer,
    )


def invite_organizer(
        to_email
):
    send_transactional_email(
        to_email,
        from_email=CONFIG.SENDGRID_ORGANIZER_FROM,
        subject=CONFIG.INVITE_SUBJECT,
        template_path="email/invite_organizer.html",
        email=to_email,
    )


def confirm_complaint(
        to_email,
        complaint,
):
    send_transactional_email(
        to_email,
        from_email=CONFIG.SENDGRID_COMPLAINT_FROM,
        subject=CONFIG.COMPLAINT_SUBJECT,
        template_path="email/confirm_complaint.html",
        complaint=complaint
    )
