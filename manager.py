import time
import os
import logging
from dotenv import load_dotenv

from monitor import TransactionMonitor
from notifier import EmailNotifier

# Load environment variables from .env file
load_dotenv()

# Failure threshold to trigger basic alerts
THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", 100))

# Multiplier to detect sudden spikes in failure count
SPIKE_MULTIPLIER = 2

# Configure basic logging output
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler("transaction_monitor.log", maxBytes=1_000_000, backupCount=3)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)


def run_monitor():
    monitor = TransactionMonitor()
    notifier = EmailNotifier()

    # Track previous failure counts for each transaction type
    last_counts = {}

    logging.info("Transaction Monitor started.")

    try:
        while True:
            # Get all transaction types with failure count > 0
            all_failures = monitor.get_high_failure_rows(threshold=0)

            # Build a dictionary of {transaction_type: failed_count}
            current_counts = {tx_type: count for tx_type, count in all_failures}

            # --- 1. Check for types that exceed the defined threshold
            current_high = {
                tx_type: count for tx_type, count in current_counts.items()
                if count > THRESHOLD
            }

            # --- 2. Detect sudden spikes compared to last known counts
            spiked = {}
            for tx_type, count in current_counts.items():
                if tx_type in last_counts:
                    previous = last_counts[tx_type]
                    if previous > 0 and count >= previous * SPIKE_MULTIPLIER:
                        spiked[tx_type] = (previous, count)

            if spiked:
                logging.warning("Sudden spikes detected in transaction failures.")

                message = " Spike Alert: Sudden Increase in Failures\n\n"
                for tx_type, (old, new) in spiked.items():
                    logging.warning(f" - {tx_type}: {old} → {new}")
                    message += f"- {tx_type}: increased from {old} to {new}\n"

                notifier.send_alert(message)

            # --- 3. Regular threshold breach alert
            if current_high:
                logging.warning("Transactions exceeding failure threshold.")

                message = " High Failed Transactions Detected:\n\n"
                for tx_type, count in current_high.items():
                    logging.warning(f" - {tx_type}: {count}")
                    message += f"- {tx_type}: {count} failed\n"

                notifier.send_alert(message)

            # --- 4. Detect transactions with 0 successful transactions
            zero_success = monitor.get_zero_success_rows()
            if zero_success:
                logging.critical(" Transaction types with zero successful transactions:")
                message = " CRITICAL: No Successful Transactions Detected\n\n"
                for tx_type in zero_success:
                    logging.critical(f" - {tx_type}: 0 successful")
                    message += f"- {tx_type}: 0 successful\n"
                notifier.send_alert(message)

            # --- 5. No problems? Celebrate.
            if not current_high and not spiked and not zero_success:
                logging.info(" All transactions within safe limits.")

            # Update previous counts for next iteration comparison
            last_counts = current_counts.copy()

            # Sleep for 60 seconds before next check
            time.sleep(60)

    except KeyboardInterrupt:
        # Allow clean exit from the infinite loop
        logging.info("Transaction Monitor stopped by user.")

# Run the monitoring loop if this script is executed directly
if __name__ == "__main__":
    run_monitor()
