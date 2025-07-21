# notifier.py
import os
import smtplib
import logging
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Set up module-level logger
logger = logging.getLogger(__name__)

class EmailNotifier:
    def send_alert(self, message_body):
        msg = EmailMessage()
        msg.set_content(message_body)

        # Create a dynamic subject line based on message type
        if "CRITICAL" in message_body:
            subject = "CRITICAL: Zero Success Detected"
        elif "Spike Alert" in message_body:
            subject = "Spike in Failures"
        elif "High Failed Transactions" in message_body:
            subject = "High Failed Transactions"
        else:
            subject = "Transaction Monitor Alert"

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
                smtp.send_message(msg)
            logger.info("Email sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
