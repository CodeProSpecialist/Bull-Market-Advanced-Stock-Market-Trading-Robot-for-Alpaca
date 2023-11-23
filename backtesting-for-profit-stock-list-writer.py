import yfinance as yf
from datetime import date, timedelta, datetime
import time
import pytz

# Function to check if a stock has increased in value by 10%
def has_increased_by_10_percent(start_value, end_value):
    return (end_value - start_value) / start_value >= 0.1

# Function to get the current date and time in Eastern Time (ET)
def get_current_time():
    eastern_tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern_tz)
    return current_time.strftime("%A, %B %d, %Y %I:%M:%S %p")

while True:
    try:
        # Read the list of stock symbols from the text file
        with open("list-of-stock-symbols-to-scan.txt", "r") as file:
            stock_symbols = file.read().splitlines()

        # Print today's date and time in Eastern Time (ET)
        print(f"Today's data in Eastern Time (ET): {get_current_time()}")
        print("")

        # Calculate the end date as today's date or the last weekday if it's a Saturday or Sunday
        today = date.today()
        if today.weekday() >= 5:  # Saturday or Sunday
            days_to_subtract = today.weekday() - 4
            end_date = today - timedelta(days=days_to_subtract)
        else:
            end_date = today

        # Calculate the start date as 2 weeks (10 trading days) before the end date
        start_date = end_date - timedelta(days=10)

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
