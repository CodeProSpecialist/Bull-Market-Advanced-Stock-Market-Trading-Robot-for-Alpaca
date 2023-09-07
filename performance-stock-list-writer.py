import time
import pytz
import yfinance as yf
from datetime import datetime, timedelta

# Function to calculate the percentage change in stock price over the past 14 days
def calculate_percentage_change(stock):
    history = stock.history(period="14d")
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    return percentage_change

# Function to check if this is the first run
def is_first_run():
    try:
        with open("run_counter.txt", "r") as counter_file:
            count = int(counter_file.read())
            return count == 0
    except FileNotFoundError:
        return True

# Function to update the run counter
def update_run_counter():
    try:
        with open("run_counter.txt", "r") as counter_file:
            count = int(counter_file.read())
        with open("run_counter.txt", "w") as counter_file:
            counter_file.write(str(count + 1))
    except FileNotFoundError:
        with open("run_counter.txt", "w") as counter_file:
            counter_file.write("1")

# Define the start and end times for when the program should run
start_time = datetime.now().replace(hour=2, minute=30, second=0, microsecond=0).time()
end_time = datetime.now().replace(hour=9, minute=25, second=0, microsecond=0).time()

# Main program loop
while True:
    try:
        # Get the current time in Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)

        # Display current date and time
        current_time = now.strftime('%A, %B %d, %Y, %I:%M:%S %p')
        print(f"Current date & time (Eastern Time): {current_time}")

        if is_first_run() or (not is_first_run() and (now.weekday() in [0, 1, 2, 3, 4] and start_time <= now.time() <= end_time)):
            # Add the code to run during the specified time range here
            if is_first_run():
                update_run_counter()

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

            # Calculate the time of the next run
            next_run = now + timedelta(hours=24)
            next_run = next_run.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
            next_run_time = next_run.strftime('%I:%M:%S %p')
            print(f"Next run will be at {next_run_time} (Eastern Time).")

            print("Stocks list updated successfully.")

        # Calculate the time until the next run
        next_run = now + timedelta(hours=24)
        next_run = next_run.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        time_until_next_run = (next_run - now).total_seconds()

        # Display the time until the next run
        print(f"Next run in {time_until_next_run / 3600} hours.")
        time.sleep(time_until_next_run)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Restarting the program in 5 minutes...")
        time.sleep(300)  # Sleep for 5 minutes before restarting
