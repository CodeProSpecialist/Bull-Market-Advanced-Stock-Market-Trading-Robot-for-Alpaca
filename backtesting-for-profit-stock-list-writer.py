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
        date(today.year, 1, 2),    # New Year's Day (Observed)
        date(today.year, 1, 16),   # Martin Luther King, Jr. Day
        date(today.year, 2, 20),   # Presidents' Day/Washington's Birthday
        date(today.year, 4, 7),    # Good Friday
        date(today.year, 5, 26),   # Friday Before Memorial Day
        date(today.year, 5, 29),   # Memorial Day
        date(today.year, 6, 19),   # Juneteenth National Independence Day
        date(today.year, 7, 3),    # Monday Before Independence Day
        date(today.year, 7, 4),    # Independence Day
        date(today.year, 9, 4),    # Labor Day
        date(today.year, 10, 9),   # Columbus Day
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

    # Check for other early closure conditions

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

# Function to handle errors and restart the program
def handle_error():
    print("An error occurred. Restarting the program in 5 seconds...")
    time.sleep(5)

# Initialize start_date and end_date outside the loop
end_date = date.today() - timedelta(days=1)  # Set end date to yesterday
start_date = end_date - timedelta(days=14)  # Set start date to 14 days ago

while True:
    try:
        # Display the date header
        print(f"Eastern Time (ET): {get_current_time()}")

        # Check if today is a market holiday or early closure
        today = date.today()
        if is_market_holiday(today):
            print("Today is a market holiday or early closure. Adjusting dates for data fetching.")
            print(f"Adjusted Start Date: {start_date}")
            print(f"Adjusted End Date: {end_date}\n")

            # Change start_date and end_date to non-holiday dates
            while is_market_holiday(start_date) or is_market_holiday(end_date):
                start_date -= timedelta(days=1)
                end_date -= timedelta(days=1)

            # Continue to the next iteration of the main loop after adjusting the dates
            continue

        # Read the list of stock symbols from the text file
        with open("list-of-stock-symbols-to-scan.txt", "r") as file:
            stock_symbols = file.read().splitlines()

        # Print today's date and time in Eastern Time (ET)
        print(f"Eastern Time (ET): {get_current_time()}")
        print("")

        # Calculate the end date as today's date or the last weekday if it's a Saturday, Sunday, or a market holiday
        end_date = calculate_end_date(today)

        # Calculate the start date as 14 days ago
        start_date = end_date - timedelta(days=14)

        # Adjust start date if it falls on a weekend
        while start_date.weekday() >= 5:
            start_date -= timedelta(days=1)

        # Ensure that the end date is not in the future
        if end_date > today:
            end_date = today

        # Perform backtesting for each stock symbol
        for symbol in stock_symbols:
            try:
                # Fetch historical data using yfinance
                data = yf.download(symbol, start=start_date, end=end_date)

                if data.empty:
                    print(f"No data available for {symbol}. Moving on to the next stock...\n")
                    continue

                # Calculate the cash allocation per stock
                cash_per_stock = 300

                # Calculate the start value of each stock by multiplying the cash allocation by the opening price on the start date
                start_value = data.loc[start_date]['Open'] * cash_per_stock

                # Calculate the end value of each stock by multiplying the cash allocation by the closing price on the end date
                end_value = data.loc[end_date]['Close'] * cash_per_stock

                # Calculate the total price change in dollars
                total_price_change = end_value - start_value

                # Calculate the total percentage of price change
                percentage_change = (total_price_change / start_value) * 100

                # Print the backtesting details to inform the user
                print(f"Backtesting Dates: {start_date} to {end_date}")
                print(f"Stock Symbol: {symbol}")
                print(f"Start Price Value: {start_value}")
                print(f"End Price Value: {end_value}")
                print(f"Total Price Change: {total_price_change}")
                print(f"Percentage Change: {percentage_change:.2f}%\n")

                # Check if the stock has increased in value by 10%
                if has_increased_by_10_percent(start_value, end_value):
                    # Append the stock symbol to the output file
                    with open("electricity-or-utility-stocks-to-buy-list.txt", "a") as output_file:
                        output_file.write(symbol + "\n")

                    # Print a message indicating that the stock is being added to the list
                    print(f"{symbol} has increased by 10% or more. Adding to the list of stocks to buy.\n")

                # Introduce a 2-second delay before moving on to the next stock symbol
                time.sleep(2)

            except Exception as stock_error:
                print(f"An error occurred for stock {symbol}: {stock_error}")
                print("Moving on to the next stock...\n")

        # Print a message to inform the user that the 10% or greater profit stocks are being written to the list of stocks to buy
        print("The following stocks with 10% or greater profit are being written to the list of stocks to buy:")
        with open("electricity-or-utility-stocks-to-buy-list.txt", "r") as output_file:
            stocks_to_buy = output_file.read().splitlines()
            for stock in stocks_to_buy:
                print(stock)
        print("")

        # Wait for 30 seconds before repeating the loop
        time.sleep(30)

    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
    except Exception as e:
        handle_error()
        continue
