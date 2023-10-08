import yfinance as yf
import time
from datetime import datetime, timedelta

# Read the list of stocks from the input file
with open("s-and-p-500-large-list-of-stocks.txt", "r") as input_file:
    stocks = input_file.read().splitlines()

# Define a function to calculate the largest price increase for a stock symbol in the past 2 years for all 12 months
def calculate_largest_price_increase(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    current_time = datetime.now()
    two_years_ago = current_time - timedelta(days=2*365)  # Calculate two years ago
    largest_increase = -float('inf')
    best_month = None

    for month in range(1, 13):
        start_date = f"{two_years_ago.year}-{month:02d}-01"
        end_date = f"{current_time.year}-{month:02d}-31"
        historical_data = stock.history(start=start_date, end=end_date)

        if not historical_data.empty:
            price_increase = (historical_data["Close"].iloc[-1] - historical_data["Close"].iloc[0]) / historical_data["Close"].iloc[0]
            if price_increase > largest_increase:
                largest_increase = price_increase
                best_month = month

    return largest_increase, best_month

# Get the current date and time
current_time = datetime.now()

# Define the target time for the next run (4:15 PM Eastern time)
target_time = current_time.replace(hour=16, minute=15, second=0, microsecond=0)

# Calculate the time difference until the next run
time_difference = target_time - current_time

# Sleep for the calculated time difference
time.sleep(time_difference.total_seconds())

# Get the current month
current_month = current_time.month

# Define a list to store the stock symbols to scan
stock_symbols_to_scan = []

# Iterate through each stock and evaluate if it should be included in the list
for stock in stocks:
    largest_increase, best_month = calculate_largest_price_increase(stock)
    
    if best_month == current_month:
        stock_symbols_to_scan.append(stock.upper())

# Write the stock symbols to scan to the output file
with open("list-of-stock-symbols-to-scan.txt", "w") as output_file:
    for stock_symbol in stock_symbols_to_scan:
        output_file.write(stock_symbol + '\n')

# Print the next run time
next_run_time = datetime.now() + timedelta(days=1)
next_run_time = next_run_time.replace(hour=16, minute=15, second=0, microsecond=0)
print(f"Next run time: {next_run_time}")
