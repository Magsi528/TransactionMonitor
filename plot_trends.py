import pandas as pd
import matplotlib.pyplot as plt

# Load the log file
df = pd.read_csv("failure_trends.csv", names=["timestamp", "transaction_type", "failed_count"])

# Convert timestamps to datetime objects
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Get unique transaction types
types = df["transaction_type"].unique()
print("Available transaction types:", types)

# Let the user choose
type_to_plot = input("Which transaction type do you want to graph? ")

# Filter and plot
filtered = df[df["transaction_type"] == type_to_plot]

if filtered.empty:
    print("No data for that transaction type.")
else:
    plt.figure(figsize=(10, 6))
    plt.plot(filtered["timestamp"], filtered["failed_count"], marker="o")
    plt.title(f"Failure Trend Over Time: {type_to_plot}")
    plt.xlabel("Time")
    plt.ylabel("Failed Transactions")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{type_to_plot}_trend.png")
    plt.show()
