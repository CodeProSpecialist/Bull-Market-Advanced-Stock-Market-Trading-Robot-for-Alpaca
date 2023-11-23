import yfinance as yf
from datetime import date, timedelta, datetime
import time
import pytz
import calendar

# Function to check if a stock has increased in value by 10%
def has_increased_by_10_percent(start_value, end_value):
    return (end_value - start_value) / start_value >= 0.1

# Function to check if today is a market holiday or an early market closure
def is_market_holiday():
    # Get the current year
    current_year = date.today().year

    # Generate the list of holidays for the current year
    holidays = []
    for month in range(1, 13):
        for day in calendar.monthcalendar(current_year, month):
            if day[month - 1] != 0:
                holidays.append((month, day[month - 1]))

    # Additional dates for early closures
    early_closure_dates = [
        (11, 24),  # The day after Thanksgiving (closes at 1 pm)
        (12, 24),  # Christmas Eve (closes early if it falls on a weekday)
        (7, 3)     # July 3 (closes early if both it and July 4 fall on a weekday)
    ]

    today = date.today()

    # Check if today is a market holiday
    is_holiday = (today.month, today.day) in holidays

    # Check if today is an early closure date
    is_early_closure = (today.month, today.day) in early_closure_dates

    # Check if the current time is after 1 pm on an early closure day
    is_after_1pm_on_early_closure = is_early_closure and datetime.now().time() >= datetime.strptime("13:00", "%H:%M").time()

    return is_holiday or is_after_1pm_on_early_closure

# Function to get the current date and time in Eastern Time (ET)
def get_current_time():
    eastern_tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern_tz)
    return current_time.strftime("%A, %B %d, %Y %I:%M:%S %p")

# Function to calculate the end date considering weekends and holidays
def calculate_end_date(today):
    end_date = today

    # If today is a Saturday or Sunday, set end date to the last weekday (Friday)
    if today.weekday() >= 5:
        days_to_subtract = today.weekday() - 4
        end_date = today - timedelta(days=days_to_subtract)

    return end_date

while True:
    try:
        # Skip fetching data if today is a market holiday or early closure
        if is_market_holiday():
            print("Today is a market holiday or early closure. Skipping data fetching.")
            # Wait for 30 seconds before repeating the loop
            time.sleep(30)
            continue

        # Read the list of stock symbols from the text file
        with open("list-of-stock-symbols-to-scan.txt", "r") as file:
            stock_symbols = file.read().splitlines()

        # Print today's date and time in Eastern Time (ET)
        print(f"Today's data in Eastern Time (ET): {get_current_time()}")
        print("")

        # Calculate the end date as today's date or the last weekday if it's a Saturday or Sunday
        today = date.today()
        end_date = calculate_end_date(today)

        # Calculate the start date as 2 weeks (10 trading days) before the end date
        start_date = end_date - timedelta(days=10)

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
                print(f"Total Price Change: {total_price_change:.2f} dollars")
                print(f"Percentage Change: {percentage_change:.2f}%")
                print("")

                # Check if the stock has increased in value by 10%
                if has_increased_by_10_percent(start_value, end_value):
                    # Print a message to inform the user before writing the stock symbol to the output file
                    print("Stock symbol with 10% or greater profit:")
                    print(symbol)
                    print("")

                    # Append the stock symbol to the output file
                    with open("electricity-or-utility-stocks-to-buy-list.txt", "a") as output_file:
                        output_file.write(symbol + "\n")

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

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)
