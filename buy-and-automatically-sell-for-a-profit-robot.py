import threading
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
        time.sleep(60)  # Sleep for 1 minute and check again


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


# the below function was recommended by Artificial Intelligence
def buy_stocks(bought_stocks, stocks_to_buy, buy_sell_lock):
    stocks_to_remove = []

    for symbol in stocks_to_buy:
        today_date = datetime.today().date()
        current_price = get_current_price(symbol)
        atr_low_price = get_atr_low_price(symbol)
        cash_available = round(float(api.get_account().cash), 2)
        cash_available -= bought_stocks.get(symbol, 0)[0] if symbol in bought_stocks else 0
        qty_of_one_stock = 1

        if cash_available > current_price and current_price <= atr_low_price:
            api.submit_order(symbol=symbol, qty=qty_of_one_stock, side='buy', type='market', time_in_force='day')
            print(f" {today_date} , Bought {qty_of_one_stock} shares of {symbol} at {current_price}")
            logging.info(f" {today_date} , Bought {qty_of_one_stock} shares of {symbol} at {current_price}")
            stocks_to_remove.append((symbol, current_price, today_date))  # Append tuple

    time.sleep(2)  # sleep a number of seconds after each buy loop

    with buy_sell_lock:
        for symbol, price, date in stocks_to_remove:  # Unpack tuple
            bought_stocks[symbol] = (round(price, 4), date)
            stocks_to_buy.remove(symbol)
            remove_symbol_from_trade_list(symbol)

        refresh_after_buy()   # this is under the f in for



# the below variable and list refresh function was recommended by Artificial Intelligence
def refresh_after_buy():
    global stocks_to_buy, bought_stocks
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = update_bought_stocks_from_api()


def update_bought_stocks_from_api():
    positions = api.list_positions()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_entry_price = position.avg_entry_price
        purchase_date = datetime.today().date()  # Set the date to today
        bought_stocks[symbol] = (float(avg_entry_price), purchase_date)
    return bought_stocks


# the below function was recommended by Artificial Intelligence
def sell_stocks(bought_stocks, buy_sell_lock):
    stocks_to_remove = []
    for symbol, (bought_price, bought_date) in bought_stocks.items():
        current_price = get_current_price(symbol)
        atr_high_price = get_atr_high_price(symbol)
        today_date = datetime.today().date()
        if current_price >= atr_high_price and today_date > bought_date:
            qty = api.get_position(symbol).qty
            api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
            print(f" {today_date}, Sold {qty} shares of {symbol} at {current_price} based on ATR high price")
            logging.info(f" {today_date}, Sold {qty} shares of {symbol} at {current_price} based on ATR high price")
            stocks_to_remove.append(symbol)  # Append symbols to remove

    time.sleep(2)  # sleep a number of seconds after each sell loop

    with buy_sell_lock:
        for symbol in stocks_to_remove:
            del bought_stocks[symbol]  # Delete symbols here
        refresh_after_sell()   # this is under the f in for


# the below variable and list refresh function was recommended by Artificial Intelligence
def refresh_after_sell():
    global bought_stocks
    bought_stocks = update_bought_stocks_from_api()


# the entire main and while True code loop was recommended by Artificial Intelligence
def main():
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = update_bought_stocks_from_api()
    buy_sell_lock = threading.Lock()  # This lock may not be necessary in a single-threaded context

    while True:
        try:
            stop_if_stock_market_is_closed()
            now = datetime.now(pytz.timezone('US/Eastern'))
            current_time_str = now.strftime("Eastern Time, %m-%d-%Y,   %I:%M:%S %p")
            cash_balance = round(float(api.get_account().cash), 2)
            print(f"{current_time_str},    Cash Balance: ${cash_balance}")

            day_trade_count = api.get_account().daytrade_count
            print(f"Current day trade number: {day_trade_count} out of 3 in 5 business days")

            stocks_to_buy = get_stocks_to_trade()
            if not bought_stocks:
                bought_stocks = update_bought_stocks_from_api()

            # Call the buy and sell functions
            buy_stocks(bought_stocks, stocks_to_buy, buy_sell_lock)
            sell_stocks(bought_stocks, buy_sell_lock)

            if DEBUG:
                print("                                                                        ")
                print("\nStocks to Purchase:")
                print("                                                                        ")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    atr_low_price = get_atr_low_price(symbol)
                    print(
                        f"Symbol: {symbol} | Current Price: {current_price} | ATR low buy signal price: {atr_low_price}")
                print("----------------------------------------------------")
                print("                                                                        ")
                print("\nStocks to Sell:")
                for symbol, _ in bought_stocks.items():  # Unpacking the symbol from the items
                    current_price = get_current_price(symbol)
                    atr_high_price = get_atr_high_price(symbol)
                    print(
                        f"Symbol: {symbol} | Current Price: {current_price} | ATR high sell signal profit price: {atr_high_price}")
                    print("----------------------------------------------------")
            time.sleep(1)  # this is under the i in if


        except Exception as e:   # this is under the t in try
            logging.error(f"Error encountered: {e}")

            time.sleep(2)


if __name__ == '__main__':
    try:
        main()

    except Exception as e:

        logging.error(f"Error encountered: {e}")

        time.sleep(2)
