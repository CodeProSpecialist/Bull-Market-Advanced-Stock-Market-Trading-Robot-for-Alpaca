import yfinance as yf
import time
from datetime import datetime, timedelta
import os
import pytz  # Import pytz for timezone handling

# Set the Eastern timezone as global for yfinance to access
eastern_timezone = pytz.timezone('US/Eastern')

# Function to format time as "Month-day-year, hh:mm:ss AM"
def format_time(dt):
    return dt.strftime("%B-%d-%Y, %I:%M:%S %p")

# Function to check if the current time is within the specified trading hours
def is_trading_hours(current_time):
    if current_time.weekday() == 0:  # Monday
        # Check if the current time is after 01:00
        return current_time.hour > 1 or (current_time.hour == 1 and current_time.minute >= 0)
    elif current_time.weekday() >= 1 and current_time.weekday() <= 4:  # Tuesday to Friday
        # Check if the current time is before 15:59
        return current_time.hour < 15 or (current_time.hour == 15 and current_time.minute <= 59)
    else:
        return False

# Read the list of stocks from the input file
with open("s-and-p-500-large-list-of-stocks.txt", "r") as input_file:
    stocks = input_file.read().splitlines()

# Define a function to calculate the largest price increase for a stock symbol in the past 2 years for all 12 months
def calculate_largest_price_increase(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    current_time = datetime.now(eastern_timezone)  # Get current time in Eastern timezone
    two_years_ago = current_time - timedelta(days=2*365)  # Calculate two years ago
    largest_increase = -float('inf')
    best_month = None

    for month in range(1, 13):
        # Calculate the last day of the current month
        last_day_of_month = (current_time.replace(day=1, month=month) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        start_date = f"{two_years_ago.year}-{month:02d}-01"
        end_date = f"{last_day_of_month.year}-{last_day_of_month.month:02d}-{last_day_of_month.day:02d}"

        # Print the Eastern Time before downloading stock information
        print(f"Eastern Time: {format_time(datetime.now(eastern_timezone))} - Downloading Stock Information for {stock_symbol}")

        historical_data = stock.history(start=start_date, end=end_date)
        time.sleep(1)  # Rate limit to 1 second per stock symbol

        if not historical_data.empty:
            price_increase = (historical_data["Close"].iloc[-1] - historical_data["Close"].iloc[0]) / historical_data["Close"].iloc[0]
            if price_increase > largest_increase:
                largest_increase = price_increase
                best_month = month

    return largest_increase, best_month

# Check if a counter file exists indicating how many times the script has run
counter_file_path = "s-and-p-500-list-printer-run-counter.txt"

if os.path.exists(counter_file_path):
    with open(counter_file_path, "r") as counter_file:
        run_count = int(counter_file.read())
else:
    run_count = 0

# Increment the run count
run_count += 1

# Write the updated run count to the counter file
with open(counter_file_path, "w") as counter_file:
    counter_file.write(str(run_count))

# Get the current date and time
current_time = datetime.now()

# Check if it's within trading hours
if is_trading_hours(current_time):
    # Get the current month
    current_month = current_time.month

    # Define a list to store the stock symbols to scan
    stock_symbols_to_scan = []

    # Iterate through each stock and evaluate if it should be included in the list
    for stock in stocks:
        largest_increase, best_month = calculate_largest_price_increase(stock)

        if best_month == current_month:
            stock_symbols_to_scan.append(stock.upper())

    # Write the stock symbols to scan to the output file with the next run time
    with open("list-of-stock-symbols-to-scan.txt", "w") as output_file:
        for stock_symbol in stock_symbols_to_scan:
            output_file.write(stock_symbol + '\n')

        # Print the next run time and write it to the file
        next_run_time = current_time + timedelta(days=1)
        if current_time.weekday() == 0:  # If it's Monday, set the next run time to 16:15
            next_run_time = next_run_time.replace(hour=16, minute=15, second=0, microsecond=0)
        else:  # For Tuesday to Friday, set the next run time to 16:15
            next_run_time = next_run_time.replace(hour=16, minute=15, second=0, microsecond=0)
        output_file.write("Next run time: " + format_time(next_run_time) + '\n')

# If this is the first run or outside of trading hours, there's no need to sleep
if run_count > 1 and is_trading_hours(current_time):
    # Calculate the time difference until the next run
    time_difference = next_run_time - current_time

    # Check if the target time is in the past, and if so, add one day to the target time
    if time_difference.total_seconds() < 0:
        next_run_time += timedelta(days=1)
        time_difference = next_run_time - current_time

    # Sleep for the calculated time difference
    time.sleep(time_difference.total_seconds())

print(f"Next run time: {format_time(next_run_time)}")
