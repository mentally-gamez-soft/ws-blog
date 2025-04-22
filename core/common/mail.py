"""Define a toolkit to send email messages asynchronously."""

import logging
from smtplib import SMTPException
from threading import Thread

from flask import current_app
from flask_mail import Message

from core import mail

logger = logging.getLogger(__name__)


def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")


def send_email(
    subject, sender, recipients, text_body, cc=None, bcc=None, html_body=None
):
    """Declare the function to send an email message.

    Args:
        subject (str): the topic of the mail message
        sender (str): the sender of the email
        recipients (str): receivers of the email
        text_body (str): the message body in plain text formet of the email
        cc (str, optional): list of recipients in copies. Defaults to None.
        bcc (str, optional): list of recipients in hidden copies. Defaults to None.
        html_body (str, optional): the message body in html formet of the email. Defaults to None.
    """
    msg = Message(
        subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc
    )
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(
        target=_send_async_email, args=(current_app._get_current_object(), msg)
    ).start()
