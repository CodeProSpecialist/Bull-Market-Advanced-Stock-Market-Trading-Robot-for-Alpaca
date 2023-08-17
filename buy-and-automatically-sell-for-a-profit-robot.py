import logging
import os,sys
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

eastern = pytz.timezone('US/Eastern')

global stock_symbols, stock_data, symbol

# Dictionary to maintain previous prices and counts
stock_data = {}


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

                       2023                      https://github.com/CodeProSpecialist

         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %I:%M:%S %p")}\n')
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        time.sleep(60)  # Sleep for 1 minute and check again


# Load stock symbols from file
def load_stock_symbols():
    with open('successful-stocks-list.txt', 'r') as f:
        return [line.strip() for line in f]


# Logging setup
logging.basicConfig(filename='log-file-of-buy-and-sell-signals.txt', level=logging.INFO)


def get_current_price(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        return stock_data.history(period="5d")["Close"].iloc[-1]  # get the latest close price
    except Exception as e:
        logging.error(f"Error fetching current price for {symbol}: {str(e)}")
        return None


def get_average_true_range(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='30d')
    atr = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=22)
    return atr[-1]


def get_day_trades_count(api):
    return api.get_account().daytrade_count


def buy_stock(symbol, price, api):
    cash_available = float(api.get_account().cash)
    if cash_available > price and api.get_account().daytrade_count < 3:
        qty = int(cash_available // price)
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='day',
        )
        logging.info(f"Bought {qty} shares of {symbol} at {price}.")
        time.sleep(300)  # Wait 5 minutes for the order to update


def sell_stock(symbol, qty, api):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day',
    )
    logging.info(f"Sold {qty} shares of {symbol}.")


def update_stock_data(symbol, current_price):
    if symbol not in stock_data:
        stock_data[symbol] = {'prev_price': current_price, 'increase_count': 0, 'decrease_count': 0}
    else:
        if current_price > stock_data[symbol]['prev_price']:
            stock_data[symbol]['increase_count'] += 1
            stock_data[symbol]['decrease_count'] = 0
        elif current_price < stock_data[symbol]['prev_price']:
            stock_data[symbol]['decrease_count'] += 1
            stock_data[symbol]['increase_count'] = 0
            stock_data[symbol]['prev_price'] = current_price


while True:
    try:
        stop_if_stock_market_is_closed()
        # Display time in Eastern Time
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        print("---------------------------------------------------")
        print(current_time.strftime('%A %B %d, %Y %I:%M:%S %p'))
        print(f"Day Trades Count: {get_day_trades_count(api)} out of 3 in 5 business days. ")
        stock_symbols = load_stock_symbols()
        for symbol in stock_symbols:

            current_price = get_current_price(symbol)
            if current_price is None:
                continue  # if we can't get a price, skip this iteration

            update_stock_data(symbol, current_price)

            print(f"Symbol: {symbol}")
            print(f"Current Price: ${current_price:.2f}")

            prev_price = stock_data[symbol].get('prev_price', None)
            formatted_price = f"{prev_price:.2f}" if prev_price is not None else 'N/A'
            print(f"Previous Buy Signal Price: ${formatted_price}")

            print(f"Price Increase Count: {stock_data[symbol]['increase_count']}")
            print(f"Price Decrease Count: {stock_data[symbol]['decrease_count']}")

            atr_value = get_average_true_range(symbol)
            buy_signal_price = float(current_price - 3 * atr_value)
            sell_signal_price = float(current_price + 3 * atr_value)

            # Check for buy and sell conditions
            if stock_data[symbol]['decrease_count'] == 5:
                buy_stock(symbol, buy_signal_price, api)
                stock_data[symbol]['decrease_count'] = 0  # Reset counter

            positions = api.list_positions()
            for position in positions:
                if position.symbol == symbol and stock_data[symbol]['decrease_count'] == 3:
                    sell_stock(symbol, int(position.qty), api)
                    stock_data[symbol]['decrease_count'] = 0  # Reset counter

        time.sleep(2)

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        time.sleep(2)  # To ensure that the loop continues even after an error