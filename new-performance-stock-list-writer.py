import time
import yfinance as yf
from datetime import datetime
import pytz  # You'll need to install pytz if you haven't already

# Function to read the list of stock symbols from a file
def read_stock_symbols(filename):
    with open(filename, 'r') as file:
        symbols = [line.strip() for line in file]
    return symbols

# Function to get the top price increase stocks for the past 5 days
def get_top_increase_stocks(symbols):
    top_stocks = {}
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist_data = stock.history(period='5d')
        if len(hist_data) == 5:
            price_increase = (hist_data['Close'][-1] - hist_data['Close'][0]) / hist_data['Close'][0]
            top_stocks[symbol] = price_increase
    return dict(sorted(top_stocks.items(), key=lambda item: item[1], reverse=True))

# Function to write the top increase stocks to an output file
def write_top_stocks_to_file(filename, top_stocks):
    with open(filename, 'w') as file:
        rank = 1
        for symbol, price_increase in top_stocks.items():
            percent_change = price_increase * 100
            change_symbol = '+' if percent_change > 0 else '-'
            file.write(f"{rank}. {symbol}: {change_symbol}{abs(percent_change):.2f}%\n")
            rank += 1

if __name__ == "__main__":
    input_filename = "list-of-stock-symbols-to-scan.txt"
    output_filename = "electricity-or-utility-stocks-to-buy-list.txt"

    # Set the timezone to Eastern Time (ET)
    et = pytz.timezone('US/Eastern')

    while True:
        # Get the current date and time in Eastern Time
        current_time = datetime.now(et)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        print(f"Eastern Time: {formatted_time}")

        stocks_to_scan = read_stock_symbols(input_filename)
        top_increase_stocks = get_top_increase_stocks(stocks_to_scan)

        # Write the top increase stocks to the output file and display on the screen
        write_top_stocks_to_file(output_filename, top_increase_stocks)
        for line in open(output_filename, 'r'):
            print(line, end='')

        # Sleep for 30 seconds before the next update
        time.sleep(30)
