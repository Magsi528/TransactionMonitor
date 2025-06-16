# notifier.py
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

class EmailNotifier:
    def send_alert(self, failed_transactions):
        msg = EmailMessage()
        msg.set_content(f"🚨 Alert! Failed Transactions = {failed_transactions} (exceeds 100)")
        msg["Subject"] = "Failed Transactions Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
                smtp.send_message(msg)
            print("📧 Email sent successfully.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
