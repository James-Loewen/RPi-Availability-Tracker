import os
import smtplib
from email.message import EmailMessage

# Sensitive info saved locally as env variables
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
RECIPIENT = os.environ.get("RECIPIENT")


# I believe this is called a void function or a procedure
# I'm not sure if this is considered best-practice or not
def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = [RECIPIENT, f"{PHONE_NUMBER}@vtext.com"]
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
