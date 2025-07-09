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

# Setup logging
logger = logging.getLogger(__name__)



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

            # Detect header row and set column indexes
            self.header_row_index, self.header_map = self._find_header_row()

        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            raise

    def _find_header_row(self):
        all_rows = self.sheet.get_all_values()
        for i, row in enumerate(all_rows):
            if "Failed Transactions" in row and "Transaction Type" in row:
                header_map = {name: idx for idx, name in enumerate(row)}
                return i, header_map
        raise ValueError("Header row with required columns not found.")

    def get_total_failed_transactions(self):
        """
        Sums all values in the 'Failed Transactions' column.
        """
        try:
            rows = self.sheet.get_all_values()[self.header_row_index + 1:]  # Skip header
            failed_idx = self.header_map["Failed Transactions"]
            total = 0
            for row in rows:
                if len(row) > failed_idx and row[failed_idx].isdigit():
                    total += int(row[failed_idx])
            return total
        except Exception as e:
            logger.error(f"Error calculating total failed transactions: {e}")
            return None

    def get_high_failure_rows(self, threshold=100):
        """
        Returns a list of (Transaction Type, Failed Count) for rows exceeding the threshold.
        """
        try:
            rows = self.sheet.get_all_values()[self.header_row_index + 1:]  # skip header
            type_idx = self.header_map["Transaction Type"]
            failed_idx = self.header_map["Failed Transactions"]
            high_failures = []

            for row in rows:
                if len(row) > failed_idx:
                    try:
                        transaction_type = row[type_idx]
                        failed_count = int(row[failed_idx])
                        if failed_count > threshold:
                            high_failures.append((transaction_type, failed_count))
                    except ValueError:
                        continue  # skip rows with non-integer counts

            return high_failures

        except Exception as e:
            logger.error(f"Error reading sheet: {e}")
            return []

    def get_zero_success_rows(self):
        """
        Returns a list of transaction types where Successful Transactions == 0
        and Total Transactions > 0 (to avoid false positives on empty rows).
        """
        try:
            rows = self.sheet.get_all_values()[self.header_row_index + 1:]  # Skip header
            type_idx = self.header_map["Transaction Type"]
            total_idx = self.header_map["Total Transactions"]
            success_idx = self.header_map["Successful Transactions"]
            zero_success = []

            for row in rows:
                if len(row) > success_idx:
                    try:
                        transaction_type = row[type_idx]
                        total = int(row[total_idx])
                        success = int(row[success_idx])
                        if total > 0 and success == 0:
                            zero_success.append(transaction_type)
                    except ValueError:
                        continue  # skip bad rows

            return zero_success

        except Exception as e:
            logger.error(f"Error checking for zero successful transactions: {e}")
            return []
