import time
import pytz
import yfinance as yf
from datetime import datetime, timedelta

# Function to calculate the percentage change in stock price over the past 14 days
def calculate_percentage_change(stock):
    # Retrieve historical data for the past 1 year
    history = stock.history(period="1y")
    
    # Calculate percentage change
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    
    return percentage_change

# Function to calculate the percentage change in stock price over the past 7 days
def calculate_7_day_percentage_change(stock):
    # Retrieve historical data for the past 7 days
    history = stock.history(period="7d")
    
    # Calculate percentage change
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    
    return percentage_change

# Function to calculate the percentage change in stock price over the past 14 days
def calculate_14_day_percentage_change(stock):
    # Retrieve historical data for the past 14 days
    history = stock.history(period="14d")
    
    # Calculate percentage change
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    
    return percentage_change

# Function to calculate the percentage change in stock price over the past 1 month
def calculate_1_month_percentage_change(stock):
    # Retrieve historical data for the past 1 month
    history = stock.history(period="1mo")
    
    # Calculate percentage change
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
start_time = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0).time()
end_time = datetime.now().replace(hour=15, minute=59, second=0, microsecond=0).time()

# Main program loop
while True:
    try:
        # Get the current time in Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)

        # Check if it's a weekday (Monday through Friday), within the specified time range, and update every 5 minutes
        if now.weekday() in [0, 1, 2, 3, 4] and start_time <= now.time() <= end_time:
            if is_first_run():
                update_run_counter()

            print("")
            print(" Performance Stock List Writer ")
            print("")

            # Read the list of stock symbols from the input file
            with open("list-of-stock-symbols-to-scan.txt", "r") as input_file:
                stock_symbols = input_file.read().splitlines()

            # Initialize a list to store stock symbols and their percentage changes
            stock_data = []

            # Fetch data for each stock symbol and calculate percentage changes
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                print("")
                print("Please wait. The stock data is being calculated right now.....")
                print("")
                time.sleep(5)  # Delay to avoid overloading the API
                percentage_change_1_year = calculate_percentage_change(stock)
                percentage_change_7_days = calculate_7_day_percentage_change(stock)
                percentage_change_14_days = calculate_14_day_percentage_change(stock)
                percentage_change_1_month = calculate_1_month_percentage_change(stock)
                stock_data.append((symbol, percentage_change_1_year, percentage_change_7_days, percentage_change_14_days, percentage_change_1_month))

            # Sort the stock data by all percentage changes in descending order
            stock_data.sort(key=lambda x: (x[1], x[2], x[3], x[4]), reverse=True)

            # Tough stock market conditions require selecting only the #1 best stock at a time to buy. 
	    # Select the top number 1 stock to buy based on all criteria
            top_stocks = stock_data[:1]

            # Erase the existing file and write the selected stock symbols to the output file
            with open("electricity-or-utility-stocks-to-buy-list.txt", "w") as output_file:
                for stock in top_stocks:
                    output_file.write(f"{stock[0]}\n")

            print("")
            print("Successful stocks list updated successfully.")
            print("")

        # Calculate the time until the next run
        if now.time() > end_time:
            # If the current time is past the end time, calculate the time until the next run for the following day
            next_run = now + timedelta(days=1, minutes=30)
            next_run = next_run.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        else:
            next_run = now + timedelta(minutes=5)
            next_run = next_run.replace(second=0, microsecond=0)

        # Update the next run time
        next_run_time = next_run.strftime('%I:%M %p')

        # Display the main message with the next run time
        main_message = f"Next run will be soon after the time of {next_run_time} (Eastern Time)."
        print(main_message)
        print("")

        # Sleep until the next run
        time_until_next_run = (next_run - now).total_seconds()
        time.sleep(time_until_next_run)

    except Exception as e:
        print("")
        print(f"An error occurred: {str(e)}")
        print("Restarting the program in 5 minutes...")
        print("")
        time.sleep(300)  # Sleep for 5 minutes before restarting
 
