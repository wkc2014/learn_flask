from flask import Flask
from flask_mail import Message, Mail

app = Flask(__name__)
mail = Mail(app)

MAIL_SERVER = 'smtp.sina.com'
MAIL_PORT = 25
MAIL_USE_TLS = 'True'
MAIL_USE_SSL = 'True'
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

def send_email():
    msg = Message("Confirm Your Account",sender='FLASKY_MAIL_SENDER', recipients=["1091416917@qq.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)


@app.route("/")
def index():
    msg = Message("Confirm Your Account", sender='FLASKY_MAIL_SENDER', recipients=["1091416917@qq.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)

if __name__ == '__main__':
    app.run()
