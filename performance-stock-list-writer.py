import time
import pytz
import yfinance as yf
from datetime import datetime, timedelta

# Define the minimum percentage change required for a 1-year increase
MIN_PERCENTAGE_CHANGE = 7.0  # Minimum 7% increase required for the entire year

# Function to calculate the percentage change in stock price over the past 1 year
def calculate_percentage_change(stock):
    # Retrieve historical data for the past 1 year
    history = stock.history(period="1y")
    
    # Calculate percentage change
    start_price = history['Open'][0]
    end_price = history['Close'][-1]
    percentage_change = ((end_price - start_price) / start_price) * 100
    
    return percentage_change

# Function to calculate the percentage change in stock price for each month of the year
def calculate_monthly_percentage_changes(stock):
    # Retrieve historical data for the past 2 years to ensure all 12 months are covered
    history = stock.history(period="2y")
    
    # Initialize a dictionary to store monthly percentage changes
    monthly_changes = {}
    
    # Loop through each month and calculate percentage change
    for month in range(1, 13):
        start_date = f"2022-{month:02d}-01"  # Start date for the specified month
        end_date = f"2023-{month:02d}-01"    # End date for the specified month
        
        # Filter historical data for the specified month
        monthly_data = history[start_date:end_date]
        
        # Calculate percentage change for the month
        if not monthly_data.empty:
            start_price = monthly_data['Open'][0]
            end_price = monthly_data['Close'][-1]
            monthly_percentage_change = ((end_price - start_price) / start_price) * 100
        else:
            # If there is no data for the month, set percentage change to 0
            monthly_percentage_change = 0.0
        
        # Store the monthly percentage change in the dictionary
        monthly_changes[month] = monthly_percentage_change
    
    return monthly_changes


# Define the start and end times for when the program should run
start_time = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0).time()
end_time = datetime.now().replace(hour=15, minute=59, second=0, microsecond=0).time()


# Your main program loop
while True:
    try:
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        
        if now.weekday() in [0, 1, 2, 3, 4]:
            # Read the list of stock symbols from the input file
            with open("list-of-stock-symbols-to-scan.txt", "r") as input_file:
                stock_symbols = [line.strip() for line in input_file if line.strip()]
            
            # Initialize a dictionary to store stock data
            stock_data = {}
            
            # Fetch historical data and calculate percentage changes for each stock
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                print(f"Fetching data for {symbol}...")
                percentage_change_1_year = calculate_percentage_change(stock)
                monthly_percentage_changes = calculate_monthly_percentage_changes(stock)
                stock_data[symbol] = {
                    'percentage_change_1_year': percentage_change_1_year,
                    'monthly_percentage_changes': monthly_percentage_changes
                }
            
            # Analyze the monthly percentage changes and select the top 28 stocks for the current month
            current_month = now.month
            current_year = now.year

            # Filter stocks based on historical performance for the current month, 1 year ago
            filtered_stocks = []
            for symbol, data in stock_data.items():
                if (
                    current_month in data['monthly_percentage_changes'] and
                    data['monthly_percentage_changes'][current_month] > 0 and
                    data['percentage_change_1_year'] >= MIN_PERCENTAGE_CHANGE
                ):
                    filtered_stocks.append((symbol, data['percentage_change_1_year']))
            
            # Sort the filtered stocks by percentage change for the current year
            sorted_stocks = sorted(filtered_stocks, key=lambda x: x[1], reverse=True)
            
            # Select the top 28 stocks
            top_stocks = sorted_stocks[:28]
            
            # Write the selected stock symbols to the output file
            with open("electricity-or-utility-stocks-to-buy-list.txt", "w") as output_file:
                for symbol, _ in top_stocks:
                    output_file.write(f"{symbol}\n")

            print("")
            print("Successful stocks list updated successfully.")
            print("")

        # Calculate the next run time
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
