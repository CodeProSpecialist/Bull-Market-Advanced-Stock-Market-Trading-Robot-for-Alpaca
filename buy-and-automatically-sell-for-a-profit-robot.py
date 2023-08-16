import logging
import os
import time
from datetime import datetime, time as time2

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


# Setting up logging
logging.basicConfig(filename="log-file-of-buy-and-sell-signals.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


def get_current_price(symbol):
    data = yf.download(tickers=symbol, period="1d", interval="1m")
    return float(data["Close"][-1])

def buy_stock(symbol):
    price = get_current_price(symbol)
    cash = float(api.get_account().cash)
    if cash > price:  # Checking if we have enough cash to buy 1 share
        try:
            api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='day')
            logging.info(f"Bought {symbol} at {price}")
            time.sleep(300)  # Wait for 5 minutes after buying
        except Exception as e:
            logging.error(f"Error buying {symbol}: {e}")

def sell_stock(symbol):
    positions = api.list_positions()
    for position in positions:
        if position.symbol == symbol:
            try:
                api.submit_order(symbol=symbol, qty=int(position.qty), side='sell', type='market', time_in_force='day')
                logging.info(f"Sold {symbol}")
            except Exception as e:
                logging.error(f"Error selling {symbol}: {e}")

with open("successful-stocks-list.txt", "r") as f:
    symbols = f.read().splitlines()

while True:
    try:
        stop_if_stock_market_is_closed()
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        current_time_str = now.strftime('%A, %B %d, %Y, %I:%M:%S %p (Eastern Time)')
        print(f"Current Time: {current_time_str}")

        # Make sure to respect Alpaca's rate limits. The default rate limit for Alpaca's API is 200 requests per minute.

        # Checking and logging owned positions
        positions = api.list_positions()
        for position in positions:
            symbol = position.symbol
            logging.info(f"Owned stock - Symbol: {symbol}, Avg purchase price: {position.avg_entry_price}, Current price: {get_current_price(symbol)}")

        for symbol in symbols:
            data = yf.download(tickers=symbol, period="22d", interval="1d")
            close = data['Close'].values
            atr = talib.ATR(data['High'].values, data['Low'].values, close, timeperiod=22)
            if close[-1] > close[-2] + 3 * atr[-2]:
                logging.info(f"Buy Signal for {symbol} - Previous Close: {close[-2]}, Current Close: {close[-1]}, ATR: {atr[-2]}")
                if api.get_account().daytrade_count < 3:  # Checking day trade count
                    buy_stock(symbol)
            elif close[-1] < close[-2] - 3 * atr[-2]:
                logging.info(f"Sell Signal for {symbol} - Previous Close: {close[-2]}, Current Close: {close[-1]}, ATR: {atr[-2]}")
                sell_stock(symbol)

            # Print each symbol's name, previous buy signal price, previous buy signal date, and current price
            print(f"Symbol: {symbol}, Previous Close: {close[-2]}, Current Price: {close[-1]}")

            time.sleep(2)  # Wait for 2 seconds before the next iteration

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    except:
        logging.error("Unexpected error in main loop.")

    time.sleep(2)



