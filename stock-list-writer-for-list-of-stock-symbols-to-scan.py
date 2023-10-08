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

# Function to read stock symbols from the input file
def read_stock_symbols(file_path):
    with open(file_path, "r") as input_file:
        return input_file.read().splitlines()

# Function to calculate the best months for a stock symbol in the past years
def calculate_best_months(stock_symbol, years_ago):
    stock = yf.Ticker(stock_symbol)
    current_time = datetime.now(eastern_timezone)  # Get current time in Eastern timezone
    years_ago_time = current_time - timedelta(days=365*years_ago)  # Calculate years ago
    best_months = {year: [] for year in range(current_time.year - years_ago, current_time.year + 1)}

    for month in range(1, 13):
        # Calculate the last day of the current month
        last_day_of_month = (years_ago_time.replace(day=1, month=month) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        start_date = f"{years_ago_time.year}-{month:02d}-01"
        end_date = f"{last_day_of_month.year}-{last_day_of_month.month:02d}-{last_day_of_month.day:02d}"

        if is_trading_hours(current_time):
            print(f"Eastern Time: {format_time(datetime.now(eastern_timezone))} - Downloading Stock Information for {stock_symbol}")
            historical_data = stock.history(start=start_date, end=end_date)
            time.sleep(1)  # Rate limit to 1 second per stock symbol

            if not historical_data.empty:
                price_increase = (historical_data["Close"].iloc[-1] - historical_data["Close"].iloc[0]) / historical_data["Close"].iloc[0]
                best_months[years_ago_time.year].append((month, price_increase))

    # Sort the best months by price increase
    for year, months in best_months.items():
        best_months[year] = [month for month, price_increase in sorted(months, key=lambda x: x[1], reverse=True)[:2]]

    return best_months

# Function to check if it's within trading hours
def is_trading_hours(current_time):
    if current_time.weekday() == 0:  # Monday
        # Check if the current time is after 01:00
        if current_time.hour > 1 or (current_time.hour == 1 and current_time.minute >= 0):
            return True
    elif current_time.weekday() >= 1 and current_time.weekday() <= 4:  # Tuesday to Friday
        # Check if the current time is before 15:59
        if current_time.hour < 15 or (current_time.hour == 15 and current_time.minute <= 59):
            return True

    return False

# Function to select and write the best-performing stocks to the output file
def select_and_write_best_stocks(stock_symbols, output_file_path):
    current_time = datetime.now()
    current_month = current_time.month
    stock_symbols_to_scan = []

    for stock_symbol in stock_symbols:
        best_months_1_year_ago = calculate_best_months(stock_symbol, 1)
        best_months_2_years_ago = calculate_best_months(stock_symbol, 2)

        if current_month in best_months_1_year_ago[current_time.year] or current_month in best_months_2_years_ago[current_time.year]:
            stock_symbols_to_scan.append(stock_symbol.upper())

    with open(output_file_path, "w") as output_file:
        for stock_symbol in stock_symbols_to_scan:
            output_file.write(stock_symbol + '\n')

        # Print the next run time
        next_run_time = current_time + timedelta(days=1)
        next_run_time = next_run_time.replace(hour=1, minute=0, second=0, microsecond=0)

        # If this is the first run, there's no need to sleep
        if run_count > 1:
            # Calculate the time difference until the next run
            time_difference = next_run_time - current_time

            # Check if the target time is in the past, and if so, add one day to the target time
            if time_difference.total_seconds() < 0:
                next_run_time += timedelta(days=1)
                time_difference = next_run_time - current_time

            # Sleep for the calculated time difference
            time.sleep(time_difference.total_seconds())

        output_file.write("Next run time: " + format_time(next_run_time) + '\n')

# Function to run the main program logic
def run_program():
    # Read the list of stock symbols
    input_file_path = "s-and-p-500-large-list-of-stocks.txt"
    stock_symbols = read_stock_symbols(input_file_path)

    # Select and write the best-performing stocks
    output_file_path = "list-of-stock-symbols-to-scan.txt"
    select_and_write_best_stocks(stock_symbols, output_file_path)

# Function to check if it's the first run of the day
def is_first_run_of_day():
    current_time = datetime.now(eastern_timezone)
    return current_time.hour == 1 and current_time.minute == 0 and current_time.second == 0

# Main program loop
while True:
    try:
        run_count = 0  # Reset run count

        # Check if it's the first run of the day
        if is_first_run_of_day():
            run_program()  # Run the program immediately on the first run
        else:
            # Sleep for 22 hours before starting again at 1:00 AM
            time.sleep(22 * 60 * 60)  # 22 hours in seconds

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting the program...")

        # Sleep for 5 minutes before restarting
        time.sleep(300)  # 300 seconds = 5 minutes
