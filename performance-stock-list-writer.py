import time
import pytz
import yfinance as yf
from datetime import datetime, timedelta

# Function to calculate the percentage increase in stock price for the month 1 year ago
def calculate_percentage_increase(stock):
    # Calculate the date one year ago from today
    one_year_ago = datetime.now() - timedelta(days=365)
    
    # Calculate the start and end date for the month one year ago
    start_date = one_year_ago.replace(day=1, hour=0, minute=0, second=0)
    end_date = one_year_ago.replace(day=one_year_ago.day, hour=23, minute=59, second=59)
    
    # Retrieve historical data for that month
    history = stock.history(start=start_date, end=end_date)
    
    # Calculate the percentage increase for the month
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_increase = ((end_price - start_price) / start_price) * 100
    
    return percentage_increase

# Function to select the top stocks to buy based on percentage increase criteria
def select_top_stocks(stock_symbols):
    selected_stocks = []

    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        print("")
        print(f"Calculating data for {symbol}...")
        print("")
        time.sleep(2)  # Delay to avoid overloading the API (1 time per 2 seconds)
        percentage_increase = calculate_percentage_increase(stock)
        
        if percentage_increase >= MIN_PERCENTAGE_CHANGE:
            selected_stocks.append((symbol, percentage_increase))

    # Sort the selected stocks by percentage increase (largest at the top)
    selected_stocks.sort(key=lambda x: x[1], reverse=True)

    return selected_stocks

# Your main program loop
# Initialize a dictionary to store stock data
stocks_by_month = {}

# Read the list of stock symbols from the input file
with open("list-of-stock-symbols-to-scan.txt", "r") as input_file:
    stock_symbols = []
    for line in input_file:
        symbol, month = line.strip().split(',')
        stock_symbols.append(symbol)

# Define the minimum percentage increase for a stock to be considered for the entire year
MIN_PERCENTAGE_CHANGE = 7.0  # Minimum 7% increase required for the entire year

# Define the start and end times for when the program should run
start_time = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0).time()
end_time = datetime.now().replace(hour=15, minute=59, second=0, microsecond=0).time()

while True:
    try:
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        
        if now.weekday() in [0, 1, 2, 3, 4]:
            # Step 2: Store all yfinance data for each stock for 1 year history
            stock_data = {}
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                print(f"Fetching data for {symbol}...")
                history = stock.history(period="1y")
                stock_data[symbol] = [(date, calculate_percentage_increase(history), open_price, close_price) for date, open_price, close_price in zip(
                    history.index, history['Open'], history['Close'])]
            
            # Step 3: Sort stocks by highest price increase % for the current month, 1 year ago
            selected_stocks = select_top_stocks(stock_symbols)

            # Step 4: Create a list of stocks from step 3 and sort them by largest price increase from the current past 7 days, past 14 days, and past 1 month
            selected_stocks.sort(key=lambda x: (x[1], calculate_7_day_percentage_change(stock_data[x[0]]), calculate_14_day_percentage_change(stock_data[x[0]]), calculate_1_month_percentage_change(stock_data[x[0]])), reverse=True)

            # Step 5: Print the final list of top 28 stocks to a text file
            with open("electricity-or-utility-stocks-to-buy-list.txt", "w") as output_file:
                for i, (stock, percentage_increase) in enumerate(selected_stocks[:28]):
                    output_file.write(f"{stock}\n")
                    if i == 27:  # Stop after printing the top 28 stocks
                        break

            print("")
            print("Successful stocks list updated successfully.")
            print("")

        if now.time() > end_time:
            next_run = now + timedelta(days=1, minutes=30)
            next_run = next_run.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        else:
            next_run = now + timedelta(minutes=5)
            next_run = next_run.replace(second=0, microsecond=0)

        main_message = f"Next run will be soon after the time of {next_run.strftime('%I:%M %p')} (Eastern Time)."
        print(main_message)
        print("")

        # Wait until after printing the list of stocks before calculating the next run time
        time_until_next_run = (next_run - now).total_seconds()
        time.sleep(time_until_next_run)

    except Exception as e:
        print("")
        print(f"An error occurred: {str(e)}")
        print("Restarting the program in 5 minutes...")
        print("")
        time.sleep(300)
