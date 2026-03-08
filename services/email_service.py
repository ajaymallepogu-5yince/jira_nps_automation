import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD


def send_email(to_email, subject, body):
    """
    Sends an HTML email. to_email can be a single address (str)
    or a list of addresses (list).
    """

    # Handle both single email string and list of emails
    if isinstance(to_email, list):
        recipients = to_email
    else:
        recipients = [to_email]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = ", ".join(recipients)

    # HTML body from summary_service
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL_SENDER,
            recipients,        # pass list — sends to all recipients
            msg.as_string()
        )