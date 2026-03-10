import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import EMAIL_SENDER, EMAIL_PASSWORD

# Logo base64 is stored in summary_service — no file needed, works on Lambda
from services.summary_service import BOS_LOGO_B64


def send_email(to_email, subject, body):
    """
    Sends an HTML email with the BOS logo embedded via CID (inline attachment).
    Works in Gmail — Gmail strips base64 img src but renders CID attachments.
    Works on AWS Lambda — no file system access needed.
    """

    if isinstance(to_email, list):
        recipients = to_email
    else:
        recipients = [to_email]

    # multipart/related = HTML with inline image attachments
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = ", ".join(recipients)

    # HTML body — summary_service already outputs src="cid:bos_logo"
    msg.attach(MIMEText(body, "html"))

    # Attach logo bytes inline — decoded from the base64 in summary_service
    logo_bytes = base64.b64decode(BOS_LOGO_B64)
    logo = MIMEImage(logo_bytes, _subtype="jpeg")
    logo.add_header("Content-ID", "<bos_logo>")
    logo.add_header("Content-Disposition", "inline", filename="bos-logo.jpg")
    msg.attach(logo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipients, msg.as_string())