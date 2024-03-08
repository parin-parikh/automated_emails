import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv 

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
sender_password = os.getenv("PASSWORD")

def read_email_addresses(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]

def send_email(subject, receiver_email):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("STRMLNE", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    # Load email template
    with open('emailTemplate.html', 'r') as file:
        email_template = file.read()

    msg.add_alternative(email_template, subtype="html")

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    # Read email addresses from file
    email_addresses = read_email_addresses('emails.txt')

    # Customize email subject
    subjectEmail = "Connecting for a Conversation about Your Website"

    # Send emails
    for email in email_addresses:
        send_email(subjectEmail, email)
    