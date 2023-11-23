import yfinance as yf
from datetime import date, timedelta, datetime
import time
import pytz
import calendar


# Function to check if a stock has increased in value by 10%
def has_increased_by_10_percent(start_value, end_value):
    return (end_value - start_value) / start_value >= 0.1


# Function to check if today is a market holiday or an early market closure
def is_market_holiday(today):
    # Define market holidays and early closure days
    market_holidays = [
        date(today.year, 1, 2),  # New Year's Day (Observed)
        date(today.year, 1, 16),  # Martin Luther King, Jr. Day
        date(today.year, 2, 20),  # Presidents' Day/Washington's Birthday
        date(today.year, 4, 7),  # Good Friday
        date(today.year, 5, 26),  # Friday Before Memorial Day
        date(today.year, 5, 29),  # Memorial Day
        date(today.year, 6, 19),  # Juneteenth National Independence Day
        date(today.year, 7, 3),  # Monday Before Independence Day
        date(today.year, 7, 4),  # Independence Day
        date(today.year, 9, 4),  # Labor Day
        date(today.year, 10, 9),  # Columbus Day
        date(today.year, 11, 10),  # Veterans Day (Observed)
        date(today.year, 11, 23),  # Thanksgiving Day
        date(today.year, 11, 24),  # Day After Thanksgiving
        date(today.year, 12, 25),  # Christmas Day
    ]

    # Check if today is a market holiday
    if today in market_holidays:
        return True

    # Check for early market closure days
    if today.weekday() == 4:  # Friday
        # The day after Thanksgiving
        if today + timedelta(days=1) in market_holidays:
            return True

    # Check for early closure on Maundy Thursday
    if today == date(today.year, 4, 6):
        return True

    # Check for early closure on the day before Independence Day
    if today == date(today.year, 7, 3):
        return True

    return False


# Function to get the current date and time in Eastern Time (ET)
def get_current_time():
    eastern_tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern_tz)
    return current_time.strftime("%A, %B %d, %Y %I:%M:%S %p")


# Function to calculate the end date considering weekends and holidays
def calculate_end_date(today):
    # If today is a market holiday, set end_date to 1 day before the market holiday
    if is_market_holiday(today):
        end_date = today - timedelta(days=1)
        while end_date.weekday() >= 5 or is_market_holiday(end_date):
            end_date -= timedelta(days=1)
    else:
        # Initialize end date as today
        end_date = today

        # Skip weekends and market holidays
        while end_date.weekday() >= 5 or is_market_holiday(end_date):
            end_date -= timedelta(days=1)

    return end_date


# Function to calculate the start date considering weekends
def calculate_start_date(end_date):
    # Initialize start date as 2 weeks (10 trading days) before the end date
    start_date = end_date - timedelta(days=10)

    # Skip weekends
    while start_date.weekday() >= 5:
        start_date -= timedelta(days=1)

    return start_date


while True:
    try:
        # Skip fetching data if today is a market holiday or early closure
        today = date.today()
        if is_market_holiday(today):
            print("Today is a market holiday or early closure. Adjusting dates for data fetching.")

            # Calculate the end date as the next available trading day
            end_date = calculate_end_date(today)

            # Calculate the start date as 2 weeks (10 trading days) before the adjusted end date
            start_date = calculate_start_date(end_date)

            print(f"Adjusted Start Date: {start_date}")
            print(f"Adjusted End Date: {end_date}")
            print("")

            # Break out of the loop after adjusting the dates
            break

        # Read the list of stock symbols from the text file
        with open("list-of-stock-symbols-to-scan.txt", "r") as file:
            stock_symbols = file.read().splitlines()

        # Print today's date and time in Eastern Time (ET)
        print(f"Today's data in Eastern Time (ET): {get_current_time()}")
        print("")

        # ... (Rest of the code remains unchanged)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)
