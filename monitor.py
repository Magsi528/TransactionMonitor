import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")

class TransactionMonitor:
    def __init__(self, creds_file='credentials.json'):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(SPREADSHEET_NAME).sheet1

    def get_failed_transactions(self):
        try:
            value = self.sheet.cell(2, 4).value
            return int(value) if value else 0
        except Exception as e:
            print(f"⚠️ Error reading sheet: {e}")
            return None
# and reading the number of failed transactions from a specific cell in the sheet.
# It uses the gspread library to interact with Google Sheets and the google-auth library for authentication.