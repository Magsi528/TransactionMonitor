# manager.py
import time
from monitor import TransactionMonitor
from notifier import EmailNotifier

THRESHOLD = 100

def run_monitor():
    monitor = TransactionMonitor()
    notifier = EmailNotifier()

    while True:
        failed_transactions = monitor.get_failed_transactions()
        print(f"📊 Failed Transactions: {failed_transactions}")

        if failed_transactions > THRESHOLD:
            notifier.send_alert(failed_transactions)
        else:
            print("✅ Transactions within safe range.")

        time.sleep(60)  # check every 60 seconds

if __name__ == "__main__":
    run_monitor()
# This code initializes the TransactionMonitor and EmailNotifier classes,
# then enters a loop that checks the number of failed transactions every 60 seconds.