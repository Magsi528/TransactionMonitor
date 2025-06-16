from monitor import TransactionMonitor

monitor = TransactionMonitor()
count = monitor.get_failed_transactions()
print(f"📊 Failed Transactions: {count}")
# This code initializes the TransactionMonitor class and retrieves the number of failed transactions from a Google Sheet.
# It prints the count of failed transactions to the console.