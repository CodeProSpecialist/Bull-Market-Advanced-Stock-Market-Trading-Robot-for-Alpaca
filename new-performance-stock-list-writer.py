import time
import yfinance as yf
from datetime import datetime, time as dt_time
import pytz  # You'll need to install pytz if you haven't already


# Function to read the list of stock symbols from a file
def read_stock_symbols(filename):
    with open(filename, 'r') as file:
        symbols = [line.strip() for line in file]
    return symbols


# Function to get the top price increase stocks for the current day
def get_top_increase_stocks(symbols):
    top_stocks = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)

            # Fetch data for only today
            hist_data = stock.history(period='1d')

            if not hist_data.empty:
                opening_price = hist_data['Open'].iloc[0]
                closing_price = hist_data['Close'].iloc[-1]
                price_increase = (closing_price - opening_price) / opening_price
                top_stocks[symbol] = price_increase
        except Exception as e:
            print(f"Error retrieving data for {symbol}: {e}")

        time.sleep(1)
    return dict(sorted(top_stocks.items(), key=lambda item: item[1], reverse=True))


# Function to print the top increase stocks to the terminal with current price
def print_top_stocks(top_stocks):
    rank = 1
    for symbol, price_increase in top_stocks.items():
        try:
            stock = yf.Ticker(symbol)
            # Fetch current price for today
            current_price = stock.history(period='1d')['Close'].iloc[-1]
            percent_change = price_increase * 100
            change_symbol = '+' if percent_change > 0 else '-'
            print(
                f"{rank}. {symbol}: ${current_price:.2f}, Open: ${stock.history(period='1d')['Open'].iloc[0]:.2f}, {change_symbol}{abs(percent_change):.2f}%")
            rank += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error printing data for {symbol}: {e}")


# Function to write the top increase stocks to an output file
def write_top_stocks_to_file(filename, top_stocks):
    with open(filename, 'w') as file:
        for symbol, price_increase in top_stocks.items():
            percent_change = price_increase * 100
            if percent_change > 0.7:
                file.write(f"{symbol}\n")


if __name__ == "__main__":
    input_filename = "list-of-stock-symbols-to-scan.txt"
    output_filename = "electricity-or-utility-stocks-to-buy-list.txt"

    # Set the timezone to Eastern Time (ET)
    et = pytz.timezone('US/Eastern')

    while True:
        try:
            # Get the current date and time in Eastern Time
            current_time = datetime.now(et)
            current_hour = current_time.hour
            current_minute = current_time.minute

            # Check if it's within market hours
            if (
                    (current_hour == 9 and current_minute >= 0) or
                    (9 < current_hour < 16) or
                    (current_hour == 16 and current_minute == 0)
            ):
                # Print only 30 minutes before market opens
                if not (current_hour == 9 and current_minute < 30):
                    print("")
                    print(f" Eastern Time: {current_time.strftime('%I:%M:%S %p | %m-%d-%Y')} ")
                    print("")

                    stocks_to_scan = read_stock_symbols(input_filename)
                    top_increase_stocks = get_top_increase_stocks(stocks_to_scan)

                    # Print the top increase stocks to the terminal
                    print_top_stocks(top_increase_stocks)

                    print("")
                    print("Writing the list of stocks: ")
                    print("")
                    # Write the top increase stocks to the output file and display on the screen
                    write_top_stocks_to_file(output_filename, top_increase_stocks)
                    for line in open(output_filename, 'r'):
                        print(line, end='')

            # Sleep for 30 seconds before the next update
            time.sleep(30)
        except Exception as e:
            print(f"Error in the main loop: {e}")
            print("Restarting the script in 1 minute...")
            time.sleep(60)
