import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

msg = EmailMessage()
msg.set_content("This is a test email from Python script.")
msg['Subject'] = "Test Email"
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
        smtp.send_message(msg)
    print("Test email sent successfully.")
except Exception as e:
    print(f"Failed to send test email: {e}")
