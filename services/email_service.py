import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import EMAIL_SENDER, EMAIL_PASSWORD

from services.summary_service import BOS_LOGO_B64


def send_email(to_email, subject, body):

    if isinstance(to_email, list):
        recipients = to_email
    else:
        recipients = [to_email]

    # Outer wrapper
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = ", ".join(recipients)

    # Inner alternative wrapper holds the HTML
    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(body, "html"))
    msg.attach(alternative)

    # Attach logo — NO Content-Disposition header so it stays hidden/inline
    logo_bytes = base64.b64decode(BOS_LOGO_B64)
    logo = MIMEImage(logo_bytes, _subtype="jpeg")
    logo.add_header("Content-ID", "<bos_logo>")
    logo["Content-Disposition"] = "inline"
    msg.attach(logo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipients, msg.as_string())