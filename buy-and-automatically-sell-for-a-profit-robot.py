import threading
import logging
import os, sys
import time
from datetime import datetime
from datetime import time as time2
import alpaca_trade_api as tradeapi
import pytz
import talib
import sqlite3
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

# the below variable was recommended by Artificial Intelligence
buy_sell_lock = threading.Lock()

logging.basicConfig(filename='log-file-of-buy-and-sell-signals.txt', level=logging.INFO)


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
        print("                                                                       ")
        print("The Stock Market Robot requires that you own at least 1 share or a fractional share of stock ")
        print("before you run the Stock Market Robot to allow the database to not be empty ")
        print("because the database can not be created when it is completely empty. ")
        print("A database needs to be created when this Stock Market Robot begins working ")
        print("to keep track of all of the stock position buying and selling. ")
        print("Thanks for understanding. Stocks can be purchased at the Alpaca website. ")
        print("This software is not affiliated or endorsed by Alpaca Securities, LLC ")
        print("This software does, however try to be a useful, profitable, and valuable ")
        print("stock market trading application. ")
        time.sleep(60)   # Sleep for 1 minute and check again


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


# the below database keeps track of bought and sold stocks, including dates
# the below database was recommended by artificial intelligence
def initialize_database():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    # Check for database corruption
    try:
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        if result[0] != 'ok':
            raise sqlite3.DatabaseError("Database is corrupted")
    except sqlite3.DatabaseError:
        # If corrupted, delete and recreate the database
        os.remove('stocks.db')
        conn = sqlite3.connect('stocks.db')
        cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS bought_stocks
                      (symbol TEXT PRIMARY KEY,
                       price REAL,
                       purchase_date TEXT)''')

    conn.commit()
    return conn


# the below code was recommended by Artificial Intelligence
def save_bought_stocks_to_database(bought_stocks, conn):
    cursor = conn.cursor()
    for symbol, (price, purchase_date) in bought_stocks.items():
        cursor.execute("INSERT OR REPLACE INTO bought_stocks (symbol, price, purchase_date) VALUES (?, ?, ?)",
                       (symbol, price, purchase_date))
    conn.commit()


# the below code was recommended by Artificial Intelligence
def load_bought_stocks_from_database(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, price, purchase_date FROM bought_stocks")
    bought_stocks = {row[0]: (row[1], datetime.strptime(row[2], "%Y-%m-%d").date()) for row in cursor.fetchall()}
    return bought_stocks


# the below code was recommended by Artificial Intelligence
def update_bought_stocks_from_api(conn):
    positions = api.list_positions()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_entry_price = position.avg_entry_price
        # Get the purchase date from the database if it exists
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_date FROM bought_stocks WHERE symbol=?", (symbol,))
        row = cursor.fetchone()
        purchase_date = datetime.strptime(row[0], "%Y-%m-%d").date() if row else datetime.today().date()
        bought_stocks[symbol] = (float(avg_entry_price), purchase_date)

    save_bought_stocks_to_database(bought_stocks, conn)
    return bought_stocks


def buy_stocks():
    with buy_sell_lock:
        global stocks_to_buy
        global bought_stocks
        global cash_balance

        stocks_to_remove = []
        for symbol in stocks_to_buy:
            current_price = get_current_price(symbol)
            atr_low_price = get_atr_low_price(symbol)
            cash_balance = round(float(api.get_account().cash), 2)
            cash_available = cash_balance - bought_stocks.get(symbol, 0)[0] if symbol in bought_stocks else cash_balance
            fractional_qty = (cash_available / current_price) * 0.025
            qty_of_one_stock = 1
            if cash_available > current_price and current_price <= atr_low_price:
                api.submit_order(symbol=symbol, qty=qty_of_one_stock, side='buy', type='market', time_in_force='day')
                print(f"Bought {qty_of_one_stock} shares of {symbol} at {current_price}")
                bought_stocks[symbol] = (round(current_price, 4), datetime.today().date())
                stocks_to_remove.append(symbol)

        for symbol in stocks_to_remove:
            stocks_to_buy.remove(symbol)
            remove_symbol_from_trade_list(symbol)
              # the buy thread will stop and allow the sell_stocks thread to keep running
        time.sleep(240)  # sleep 240 seconds after each buy order
        refresh_after_buy()   # this was recommended by Artificial Intelligence


# the below variable and list refresh function was recommended by Artificial Intelligence
def refresh_after_buy():
    global stocks_to_buy, bought_stocks
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = update_bought_stocks_from_api()


def sell_stocks():
    with buy_sell_lock:
        global bought_stocks

        for symbol, (bought_price, bought_date) in bought_stocks.items():
            current_price = get_current_price(symbol)
            atr_high_price = get_atr_high_price(symbol)
            today_date = datetime.today().date()
            if current_price >= atr_high_price and today_date > bought_date:
                qty = api.get_position(symbol).qty
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
                print(f"Sold {qty} shares of {symbol} at {current_price} based on ATR high price")
                del bought_stocks[symbol]
                time.sleep(120)  # sleep 120 seconds after each sell order
                refresh_after_sell()   # this was recommended by Artificial Intelligence


# the below variable and list refresh function was recommended by Artificial Intelligence
def refresh_after_sell():
    global bought_stocks
    bought_stocks = update_bought_stocks_from_api()


def main():
    # the below code was recommended by Artificial Intelligence
    conn = initialize_database()
    global stocks_to_buy
    global bought_stocks

    stocks_to_buy = []
    stocks_to_buy = get_stocks_to_trade()

    # Load bought_stocks when starting a brand-new instance of the program
    # the below code was recommended by Artificial Intelligence
    # Use database functions instead of file-based functions
    bought_stocks = load_bought_stocks_from_database(conn)

    if not bought_stocks:
        print("Database is empty. Please purchase at least 1 share of stock before running this Stock Market Robot.")
        print("The Stock Market Robot requires that you own at least 1 share or a fractional share of stock ")
        print("before you run the Stock Market Robot to allow the database to not be empty ")
        print("because the database can not be created when it is completely empty. ")
        print("A database needs to be created when this Stock Market Robot begins working ")
        print("to keep track of all of the stock position buying and selling. ")
        print("Thanks for understanding. Stocks can be purchased at the Alpaca website. ")
        print("This software is not affiliated or endorsed by Alpaca Securities, LLC ")
        print("This software does, however try to be a useful, profitable, and valuable ")
        print("stock market trading application. ")
        bought_stocks = update_bought_stocks_from_api(conn)

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

            # the below code was recommended by Artificial Intelligence
            # Load bought_stocks from the database
            bought_stocks = load_bought_stocks_from_database(conn)

            # the below code was recommended by Artificial Intelligence
            if not bought_stocks:
                bought_stocks = update_bought_stocks_from_api(conn)  # Include conn argument

            # Create and start the buying and selling threads
            buy_thread = threading.Thread(target=buy_stocks)   # keep the buy and sell thread lines to the far left
            # for the "b" in buy to be in the same line as the "i" in the above if not statement.
            # or else this code will not be in the main loop to buy and sell stocks.
            buy_thread.start()   # keep the buy and sell thread lines to the far left
            sell_thread = threading.Thread(target=sell_stocks)   # keep the buy and sell thread lines to the far left
            sell_thread.start()   # keep the buy and sell thread lines to the far left
            buy_thread.join()   # keep the buy and sell thread lines to the far left
            sell_thread.join()  # keep the buy and sell thread lines to the far left

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
            time.sleep(1)  # wait 1 second

        except Exception as e:
            logging.error(f"Error encountered: {e}")
            time.sleep(2)  # To ensure that the loop continues even after an error


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Error encountered: {e}")
        time.sleep(2)  # To ensure that the loop continues even after an error
