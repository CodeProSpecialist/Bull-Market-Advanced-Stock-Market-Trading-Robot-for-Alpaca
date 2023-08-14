import os
import time
import pandas as pd
import yfinance as yf
import talib
import alpaca_trade_api as tradeapi
import pytz
from datetime import datetime, timedelta, date
from datetime import time as time2
import matplotlib.pyplot as plt
import numpy as np
import logging

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

# Using pandas datareader override
yf.pdr_override()

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

eastern = pytz.timezone('US/Eastern')

debug_mode = False

global risk, symbol, data, df, stock_symbols, stock_data

risk = 0.025

filename1 = 'successful-stocks-list.txt'


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


def load_stocks_list():
    with open('successful-stocks-list.txt', 'r') as file:
        return [line.strip() for line in file]

SYMBOLS = []

SYMBOLS = load_stocks_list()


def get_stock_info(SYMBOLS):
    end = date.today() + timedelta(days=1)
    start = end - timedelta(days=364)

    stock_data = yf.download(SYMBOLS, start=start, end=end)  # This will include 'High' and 'Low' by default
    return stock_data


def compute_macd(df):
    for symbol in SYMBOLS:
        close_data = df['Close'][symbol]
        macd = talib.macd(close_data)
        df['MACD', symbol] = macd['MACD_12_26_9']
        df['MACDs', symbol] = macd['MACDs_12_26_9']
        df['MACDh', symbol] = macd['MACDh_12_26_9']
    return df


# the python code below will remove the stock from the text file after the buy order is placed
def remove_symbol(symbol, filename1):
    symbols = []
    SYMBOLS = []
    try:
        with open(filename1, 'r') as file:
            symbols = [line.strip() for line in file.readlines() if line.strip() != symbol]
    except FileNotFoundError:
        print(f"Error: File '{filename1}' not found.")
        return

    with open(filename1, 'w') as file:
        for s in symbols:
            file.write(s + "\n")

    # Clear the 'symbols' and 'SYMBOLS' variables
    SYMBOLS = load_stocks_list()

    symbols.clear()
    SYMBOLS.clear()

    # Update the 'symbols' and 'SYMBOLS' variables with new information
    symbols = load_stocks_list()
    SYMBOLS = load_stocks_list()


def MACD_Strategy(df, risk):
    MACD_Buy = []
    MACD_Sell = []
    position = False

    for i in range(0, len(df)):
        if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i]:
            MACD_Sell.append(np.nan)
            if position == False:
                MACD_Buy.append(df['Close'][i])
                position = True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i]:
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(df['Close'][i])
                position = False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and df['Close'][i] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and df['Close'][i] < df['Close'][i - 1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell

    return df


# Your MACD strategy function
def MACD_color(df):
    MACD_color = []
    for i in range(1, len(df)):  # Start from index 1 to avoid accessing index -1
        if df['MACDh_12_26_9'][i] > df['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color


def plot_graph(stocks):
    atr_period = 22
    atr_multiplier = 3

    # If your data includes multiple stocks, iterate through the symbols
    for symbol in stocks['Close'].columns:
        data = pd.DataFrame({
            'High': stocks['High'][symbol],
            'Low': stocks['Low'][symbol],
            'Close': stocks['Close'][symbol]
        })

        # Calculate ATR
        data['ATR'] = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=atr_period)

        # Calculate buy and sell signals
        data['Buy_Signal'] = data['Close'] - atr_multiplier * data['ATR']
        data['Sell_Signal'] = data['Close'] + atr_multiplier * data['ATR']

        plt.figure(figsize=(10, 6))
        plt.title(f"{symbol} Stock Price")
        plt.plot(data['Close'], label="Close Price", alpha=0.5)
        plt.plot(data['Buy_Signal'], label="Buy Signal", linestyle="--")
        plt.plot(data['Sell_Signal'], label="Sell Signal", linestyle="--")
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend(loc='best')
        plt.show()


# sell all owned stocks that lose value more than a strict minimum average of -1.0 percent: 0.99
def sell_decreasing_stocks(api):
    try:
        positions = api.list_positions()
        for position in positions:
            symbol = position.symbol
            qty = int(position.qty)
            current_price = api.get_latest_trade(symbol).price
            purchase_price = float(position.avg_entry_price)

            if current_price <= purchase_price * 0.99:  # 1.0% decrease
                make_order(api, symbol, qty, 'sell')
                log_order(symbol, 'Sold')
                print(f"Sold {symbol} as the price decreased by 1.0% or more.")
    except Exception as e:
        print(f"An error occurred while trying to sell decreasing stocks: {e}")


def make_order(api, symbol, qty, side):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type='market',
        time_in_force='day'
    )


def log_order(symbol, action):
    with open('log.txt', 'a') as f:
        f.write(f"{datetime.now()}: {action} {symbol}\n")


def check_cash(api, symbol):
    account = api.get_account()
    cash_available = float(account.cash)
    last_price = api.get_last_trade(symbol).price
    qty = int(cash_available / last_price)
    return qty if qty > 0 else None


def get_position_qty(api, symbol):
    try:
        position = api.get_position(symbol)
        return int(position.qty)
    except Exception as e:
        return None


def backtest():
    while True:
        try:
            stop_if_stock_market_is_closed()
            global SYMBOLS  # Declare SYMBOLS as a global variable
            SYMBOLS = load_stocks_list()

            # Get data once and store it in all_data
            all_data = get_stock_info(SYMBOLS)

            print(f' Eastern Time: {datetime.now(eastern).strftime("%A, %B %d, %Y %I:%M:%S %p")}')

            sell_decreasing_stocks(api)

            positions = api.list_positions()

            if positions:
                print("Stocks in our Portfolio:")
                for position in positions:
                    print(f'{position.symbol}, Current Price: {round(float(position.current_price), 2)}')
            else:
                print("No stocks are in our portfolio..... not looking to sell stocks right now.")

            # Check day trade count
            account = api.get_account()
            day_trade_count = account.daytrade_count
            print(f"Day Trade Count: {day_trade_count} out of 3 in 5 business days. ")

            if debug_mode:
                plot_graph(all_data)

            print("Stocks to buy:")
            for symbol in SYMBOLS:
                if day_trade_count <= 3:  # Check day trade count before buying
                    try:
                        df = all_data[all_data['symbol'] == symbol] # Assuming all_data contains data for all symbols and has a 'symbol' column

                        # Apply both strategies
                        df = MACD_Strategy(df, risk)

                        for i in range(len(df)):
                            print(f"Index: {i}, Date: {df.index[i]}, Buy Signal: {df['MACD_Buy_Signal_price'][i]}, Sell Signal: {df['MACD_Sell_Signal_price'][i]}")
                            # Continue with the rest of the code as before

                    except KeyError:
                        print(f"An error occurred: {symbol}")

            time.sleep(2)  # Sleep for 2 seconds and then check again

        except Exception as e:
            print(f'An error occurred: {e}')
            time.sleep(2)


if __name__ == "__main__":
    try:
        backtest()

    except KeyboardInterrupt:
        print('Interrupted by user')

    time.sleep(2)
