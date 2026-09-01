import os
from threading import Thread

from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Basic configuration for the Flask email service
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

print("User:", app.config['MAIL_USERNAME'])
print("Pass:", app.config['MAIL_PASSWORD'])

mail = Mail(app)

def send_async_email(app, msg):
    """Send the email asynchronously"""
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """Send an email main function"""
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@app.route('/hello')
def test_email():
    """
        This route should invoke the send_email() function 
        and send a test email to my email address.
    """
    send_email(
        to='khanhduy27422@gmail.com',
        subject='Hello World',
        template='hello'
    )
    return "Test email sent"

# Small note: The environment variables cannot be accessed via .env file,
# so I have to set them in the terminal before running the app.
# Actually, that did not work, so I installed python-dotenv and 
# added the print statements to check if the environment var are accessed.
# It showed work.
