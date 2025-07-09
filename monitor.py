import os
import gspread
import logging
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

# Constants
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
if not SPREADSHEET_ID:
    raise ValueError("SPREADSHEET_ID is not set in the environment.")

TRANSACTION_TYPE_COL = 1  # Column B (0-indexed in code)
FAILED_COUNT_COL = 3      # Column D

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TransactionMonitor:
    def __init__(self, creds_file='credentials.json'):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        try:
            self.creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open_by_key(SPREADSHEET_ID).sheet1
            logger.info(f"Connected to spreadsheet: {SPREADSHEET_ID}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            raise

    def get_total_failed_transactions(self):
        """
        Sums all values in the 'Failed Transactions' column.
        """
        try:
            rows = self.sheet.get_all_values()[1:]  # Skip header
            total = 0
            for row in rows:
                if len(row) > FAILED_COUNT_COL and row[FAILED_COUNT_COL].isdigit():
                    total += int(row[FAILED_COUNT_COL])
            return total
        except Exception as e:
            logger.error(f"Error calculating total failed transactions: {e}")
            return None

    def get_high_failure_rows(self, threshold=100):
        """
        Returns a list of (Transaction Type, Failed Count) for rows exceeding the threshold.
        """
        try:
            rows = self.sheet.get_all_values()[1:]  # skip header
            high_failures = []

            for row in rows:
                if len(row) > FAILED_COUNT_COL:
                    try:
                        transaction_type = row[TRANSACTION_TYPE_COL]
                        failed_count = int(row[FAILED_COUNT_COL])
                        if failed_count > threshold:
                            high_failures.append((transaction_type, failed_count))
                    except ValueError:
                        continue  # skip rows with non-integer counts

            return high_failures

        except Exception as e:
            logger.error(f"Error reading sheet: {e}")
            return []
