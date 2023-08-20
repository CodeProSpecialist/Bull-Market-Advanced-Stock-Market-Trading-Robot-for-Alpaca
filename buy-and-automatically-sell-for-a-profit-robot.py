import logging
import os, sys
import time
from datetime import datetime
from datetime import time as time2
import alpaca_trade_api as tradeapi
import pytz
import talib
import yfinance as yf

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

DEBUG = False

eastern = pytz.timezone('US/Eastern')

# Dictionary to maintain previous prices and price increase and price decrease counts
stock_data = {}

global stocks_to_buy


def stop_if_stock_market_is_closed():
    # Check if the current time is within the stock market hours
    # Set the stock market open and close times
    market_open_time = time2(9, 30)
    market_close_time = time2(16, 0)

    while True:
        # Get the current time in Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        current_time = now.time()

        # Check if the current time is within market hours
        if now.weekday() <= 4 and market_open_time <= current_time <= market_close_time:
            break

        print('''
           _____   __                   __             ____            __            __ 
          / ___/  / /_  ____   _____   / /__          / __ \  ____    / /_   ____   / /_
          \__ \  / __/ / __ \ / ___/  / //_/         / /_/ / / __ \  / __ \ / __ \ / __/
         ___/ / / /_  / /_/ // /__   / ,<           / _, _/ / /_/ / / /_/ // /_/ // /_  
        /____/  \__/  \____/ \___/  /_/|_|         /_/ |_|  \____/ /_.___/ \____/ \__/  

                       2023                       https://github.com/CodeProSpecialist

         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %I:%M:%S %p")}\n')
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        print("                                                                       ")
        print("This program will only work correctly if there is at least 1 stock symbol ")
        print("in the file named electricity-or-utility-stocks-to-buy-list.txt ")
        time.sleep(60)  # Sleep for 1 minute and check again


logging.basicConfig(filename='log-file-of-buy-and-sell-signals.txt', level=logging.INFO)


def get_stocks_to_trade():
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]


def remove_symbol_from_trade_list(symbol):
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
        lines = file.readlines()

    with open('electricity-or-utility-stocks-to-buy-list.txt', 'w') as file:
        for line in lines:
            if line.strip() != symbol:
                file.write(line)


def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="5d")["Close"].iloc[-1], 4)


def get_atr_high_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price + 3 * atr_value, 4)


def get_atr_low_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price - 3 * atr_value, 4)


def get_average_true_range(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='30d')
    atr = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=22)
    return atr[-1]


def save_bought_stocks_to_file(bought_stocks):
    with open('stock-database.txt', 'w') as file:
        for symbol, (price, purchase_date) in bought_stocks.items():
            file.write(f"{symbol} {price} {purchase_date}\n")


def load_bought_stocks_from_file():
    bought_stocks = {}
    try:
        with open('stock-database.txt', 'r') as file:
            for line in file.readlines():
                parts = line.strip().split()
                symbol = parts[0]
                price = float(parts[1])
                # If the purchase date is available, use it; otherwise, use today's date
                purchase_date = datetime.strptime(parts[2], "%Y-%m-%d").date() if len(
                    parts) > 2 else datetime.today().date()
                bought_stocks[symbol] = (price, purchase_date)
    except FileNotFoundError:
        pass

    return bought_stocks


def update_bought_stocks_from_api():
    positions = api.list_positions()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_entry_price = position.avg_entry_price
        # Use today's date as the purchase date
        purchase_date = datetime.today().date()
        bought_stocks[symbol] = (float(avg_entry_price), purchase_date)

    # Save to file
    save_bought_stocks_to_file(bought_stocks)

    return bought_stocks


def main():
    global stocks_to_buy
    global bought_stocks

    stocks_to_buy = []
    stocks_to_buy = get_stocks_to_trade()

    # Load bought_stocks from the Alpaca server API when starting a brand-new instance of the program
    bought_stocks = update_bought_stocks_from_api()

    while True:
        try:
            pass

            stop_if_stock_market_is_closed()
            now = datetime.now(pytz.timezone('US/Eastern'))
            current_time_str = now.strftime("Eastern Time, %m-%d-%Y,   %I:%M:%S %p")
            cash_balance = round(float(api.get_account().cash), 2)

            # Print the current details
            print("                                                                        ")
            print(f"{current_time_str},    Cash Balance: ${cash_balance}")

            # Get the day trade count
            day_trade_count = api.get_account().daytrade_count
            print("                                                                        ")
            print(f"Current day trade number: {day_trade_count} out of 3 in 5 business days")
            print("                                                                        ")

            stocks_to_buy = get_stocks_to_trade()

            # Load bought_stocks from the file or update from the API
            bought_stocks = load_bought_stocks_from_file()
            if not bought_stocks:
                bought_stocks = update_bought_stocks_from_api()

            stocks_to_remove = []  # a new variable for a list of stocks to remove
            for symbol in stocks_to_buy:
                current_price = get_current_price(symbol)
                atr_low_price = get_atr_low_price(symbol)  # Get the ATR low price for the symbol
                cash_available = cash_balance - bought_stocks.get(symbol, 0)[
                    0] if symbol in bought_stocks else cash_balance
                fractional_qty = (cash_available / current_price) * 0.025
                if cash_available > current_price and current_price <= atr_low_price:  # Check if the current price is less than or equal to ATR low price
                    api.submit_order(symbol=symbol, qty=fractional_qty, side='buy', type='market', time_in_force='day')
                    print(f"Bought {fractional_qty} shares of {symbol} at {current_price}")
                    bought_stocks[symbol] = (round(current_price, 4), datetime.today().date())
                    stocks_to_remove.append(symbol)  # Append or add the symbol to a list of stocks to remove
                    logging.info(
                        f"Bought {fractional_qty} shares of {symbol} at {current_price}")  # Logging the buy order

                    for symbol in stocks_to_remove:
                        stocks_to_buy.remove(symbol)  # Remove the symbol from the original variable memory list after
                        # placing a buy order for the stock symbol
                        remove_symbol_from_trade_list(symbol)  # Remove the symbol from the text file

            # Check for selling condition within bought_stocks based on ATR
            for symbol, (bought_price, bought_date) in bought_stocks.items():
                current_price = get_current_price(symbol)
                atr_high_price = get_atr_high_price(symbol)
                today_date = datetime.today().date()
                bought_date = bought_date  # Assuming the date is already a date object, otherwise convert the dates
                # into exactly the same date format.

                if current_price >= atr_high_price and today_date > bought_date:
                    qty = api.get_position(symbol).qty
                    api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
                    print(f"Sold {qty} shares of {symbol} at {current_price} based on ATR high price")
                    logging.info(f"Sold {qty} shares of {symbol} at {current_price} based on ATR high price")  # Logging the sell order
                    del bought_stocks[symbol]

            if DEBUG:
                print("                                                                        ")
                print("\nStocks to Purchase:")
                print("                                                                        ")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    atr_low_price = get_atr_low_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} | ATR low buy signal price: {atr_low_price}")
                print("----------------------------------------------------")
                print("                                                                        ")
                print("\nStocks to Sell:")
                for symbol, _ in bought_stocks.items():  # Unpacking the symbol from the items
                    current_price = get_current_price(symbol)
                    atr_high_price = get_atr_high_price(symbol)
                    print(
                        f"Symbol: {symbol} | Current Price: {current_price} | ATR high sell signal profit price: {atr_high_price}")
                    print("----------------------------------------------------")
            time.sleep(0.5)  # uncomment this line if the program is going too fast.

        except Exception as e:
            logging.error(f"Error encountered: {e}")
            time.sleep(2)  # To ensure that the loop continues even after an error


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Error encountered: {e}")
        time.sleep(2)  # To ensure that the loop continues even after an error
