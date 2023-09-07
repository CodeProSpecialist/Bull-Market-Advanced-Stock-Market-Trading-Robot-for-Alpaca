import time
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# Function to calculate the percentage change in stock price over the past 14 days
def calculate_percentage_change(stock):
    history = stock.history(period="14d")
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    return percentage_change

# Function to check if the current time is within the specified time range
def is_within_time_range(start_time, end_time):
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern).time()
    return start_time <= now <= end_time

# Define the start and end times for when the program should run
start_time = datetime.now().replace(hour=2, minute=30, second=0, microsecond=0).time()
end_time = datetime.now().replace(hour=9, minute=25, second=0, microsecond=0).time()

# Run the program every 48 hours (2 days)
interval_hours = 48

while True:
    try:
        # Get the current day of the week
        current_day = datetime.now(pytz.timezone('US/Eastern')).weekday()

        if current_day in [0, 2, 4] and is_within_time_range(start_time, end_time):
            # Add the code to run during the specified time range here
            # Read the list of stock symbols from the input file
            with open("list-of-stock-symbols-to-scan.txt", "r") as input_file:
                stock_symbols = input_file.read().splitlines()

            # Initialize a list to store stock symbols and their percentage changes
            stock_data = []

            # Fetch data for each stock symbol and calculate percentage change
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                print("Please wait. The stock data is being calculated right now.....")
                time.sleep(1.75)  # Delay to avoid overloading the API
                percentage_change = calculate_percentage_change(stock)
                stock_data.append((symbol, percentage_change))

            # Sort the stock data by percentage change in descending order
            stock_data.sort(key=lambda x: x[1], reverse=True)

            # Select the top 15 stocks
            top_stocks = stock_data[:15]

            # Erase the existing file and write only the stock symbols to the output file
            with open("electricity-or-utility-stocks-to-buy-list.txt", "w") as output_file:
                for stock in top_stocks:
                    output_file.write(f"{stock[0]}\n")

            print("Stocks list updated successfully.")

        elif current_day == 0:  # Monday
            # Calculate the time until the next run on Wednesday
            next_run = datetime.now(pytz.timezone('US/Eastern')) + timedelta(days=2)
            next_run = next_run.replace(hour=2, minute=30, second=0, microsecond=0)
            time_until_next_run = (next_run - datetime.now(pytz.timezone('US/Eastern'))).total_seconds()
            print(f"Next run will be on Wednesday at 2:30 AM. Waiting for {time_until_next_run / 3600} hours.")
            time.sleep(time_until_next_run)

        elif current_day == 2:  # Wednesday
            # Calculate the time until the next run on Friday
            next_run = datetime.now(pytz.timezone('US/Eastern')) + timedelta(days=2)
            next_run = next_run.replace(hour=2, minute=30, second=0, microsecond=0)
            time_until_next_run = (next_run - datetime.now(pytz.timezone('US/Eastern'))).total_seconds()
            print(f"Next run will be on Friday at 2:30 AM. Waiting for {time_until_next_run / 3600} hours.")
            time.sleep(time_until_next_run)

        elif current_day == 4:  # Friday
            # Calculate the time until the next run on Monday
            next_run = datetime.now(pytz.timezone('US/Eastern')) + timedelta(days=3)
            next_run = next_run.replace(hour=2, minute=30, second=0, microsecond=0)
            time_until_next_run = (next_run - datetime.now(pytz.timezone('US/Eastern'))).total_seconds()
            print(f"Next run will be on Monday at 2:30 AM. Waiting for {time_until_next_run / 3600} hours.")
            time.sleep(time_until_next_run)

        # Calculate the time until the next run
        now = datetime.now(pytz.timezone('US/Eastern'))
        next_run = now + timedelta(hours=interval_hours)
        time_until_next_run = (next_run - now).total_seconds()

        # Sleep until the next run
        print(f"Next run in {time_until_next_run / 3600} hours.")
        time.sleep(time_until_next_run)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Restarting the program in 5 minutes...")
        time.sleep(300)  # Sleep for 5 minutes before restarting
