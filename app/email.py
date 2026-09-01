"""
    This module provides functions to send emails using Flask-Mail.
    send_email() crafts the email message and start a thread
    send_async_email() works in the background hanlding the email sending process.
"""
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from . import mail # import the mail instance

def send_async_email(app, msg):
    """
        Send the email asynchronously to avoid blocking the main thread.
    """
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """
        Send an email asynchronously.
    """
    app = current_app._get_current_object() # pylint: disable=protected-access
    # Extract the actual application instance

    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    return thr
