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
        print("Stocks will strictly only be purchased at 3:50pm Eastern Time to maximize profits and to increase ")
        print("the number of stocks traded per day to the maximum number of positions. ")
        time.sleep(60)  # Sleep for 1 minute and check again


logging.basicConfig(filename='log-file-of-buy-and-sell-signals.txt', level=logging.INFO)

def get_stocks_to_trade():
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return stock_data.history(period="5d")["Close"].iloc[-1]

def get_atr_high_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return current_price + 3 * atr_value

def get_average_true_range(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='30d')
    atr = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=22)
    return atr[-1]

def main():
    api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)   # Setup your API credentials here
    stocks_to_trade = get_stocks_to_trade()
    bought_stocks = {}

    while True:
        stop_if_stock_market_is_closed()
        now = datetime.now(pytz.timezone('US/Eastern'))
        current_time_str = now.strftime("%m-%d-%Y %I:%M:%S %p")
        cash_balance = round(float(api.get_account().cash), 2)

         # Update the bought_stocks dictionary with current owned positions
        positions = api.list_positions()
        for position in positions:
            if position.symbol in stocks_to_trade:
                bought_stocks[position.symbol] = float(position.avg_entry_price)
        
        # Print the current details
        print(f"{current_time_str} - Cash Balance: ${cash_balance}")
        
        print("Stocks will strictly only be purchased at 3:50pm Eastern Time to maximize profits and to increase ")
        print("the number of stocks traded per day to the maximum number of positions. ")

        # Buy stocks at 15:50 Eastern Time
        if now.hour == 15 and now.minute == 50:
            for symbol in stocks_to_trade[:]: # Create a copy of the list to iterate over
                current_price = get_current_price(symbol)
                cash_available = cash_balance - bought_stocks.get(symbol, 0)
                fractional_qty = (cash_available / current_price) * 0.025
                if cash_available > current_price:
                    api.submit_order(symbol=symbol, qty=fractional_qty, side='buy', type='market', time_in_force='day')
                    print(f"Bought {fractional_qty} shares of {symbol} at {current_price}")
                    bought_stocks[symbol] = current_price
                    stocks_to_trade.remove(symbol) # Remove the symbol from the list after buying
        
        # Check for selling condition based on ATR
        for symbol, bought_price in bought_stocks.items():
            current_price = get_current_price(symbol)
            atr_high_price = get_atr_high_price(symbol)
            if current_price >= atr_high_price:
                qty = api.get_position(symbol).qty
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
                print(f"Sold {qty} shares of {symbol} at {current_price} based on ATR high price")
                del bought_stocks[symbol]

        time.sleep(2)

if __name__ == '__main__':
    try:
        pass
        main()
    

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        time.sleep(2)  # To ensure that the loop continues even after an error
