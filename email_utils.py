import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))

def send_confirmation_email(details, meeting_link):

    for recipient in details['attendees']:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = f"Meeting Confirmation – {details['purpose']}"

        body = f"""
        Hello,

        ✅ Your meeting has been scheduled successfully!

        📅 Purpose: {details['purpose']}
        🕒 Date & Time: {details['date_time']}
        👥 Attendees: {', '.join(details['attendees'])}
        💻 Platform: {details['platform']}
        🔗 Meeting Link: {meeting_link}

        Please mark your calendar.

        — SmartSchedulerGPT
        """

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

