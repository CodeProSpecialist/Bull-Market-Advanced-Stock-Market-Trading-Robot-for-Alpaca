import os
import time
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import pandas_datareader.data as web
import alpaca_trade_api as tradeapi
import pytz
from datetime import datetime
from datetime import time as time2
import matplotlib.pyplot as plt
import numpy as np
import logging

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# Using five thirty eight style for plots
plt.style.use('fivethirtyeight')

# Using pandas datareader override
yf.pdr_override()

eastern = pytz.timezone('US/Eastern')
debug_mode = True

global risk

risk = 0.025

filename1 = 'successful-stocks-list.txt'


def load_stocks_list():
    with open('successful-stocks-list.txt', 'r') as file:
        return [line.strip() for line in file]


def get_data(symbol):
    return yf.download(symbol, period='1d', interval='1m')


# the python code below will remove the stock from the text file after the buy order is placed
def remove_symbol(symbol, filename1):
    symbols = []
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


def OCC_Strategy(df):
    occ_signal_buy = []
    occ_signal_sell = []
    position = False

    atr = ta.atr(df.High, df.Low, df.Close, length=22)
    zema = ta.zema(df.Close)
    upper = zema + (atr * 3)
    lower = zema - (atr * 3)

    for i in range(1, len(df)):
        if df['Close'][i] > upper[i] and df['Close'][i - 1] <= upper[i - 1] and not position:
            occ_signal_buy.append(df['Close'][i])
            occ_signal_sell.append(np.nan)
            position = True
        elif df['Close'][i] < lower[i] and df['Close'][i - 1] >= lower[i - 1] and position:
            occ_signal_buy.append(np.nan)
            occ_signal_sell.append(df['Close'][i])
            position = False
        else:
            occ_signal_buy.append(np.nan)
            occ_signal_sell.append(np.nan)

    df['Buy_Signal_price'] = occ_signal_buy
    df['Sell_Signal_price'] = occ_signal_sell
    df['Zema'] = zema
    df['Upper'] = upper
    df['Lower'] = lower


def plot_graph(data, symbol):
    plt.figure(figsize=(20, 10))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['Zema'], label='ZEMA', alpha=0.5, color='blue')
    plt.plot(data['Upper'], label='Upper Bound', alpha=0.5, color='green')
    plt.plot(data['Lower'], label='Lower Bound', alpha=0.5, color='red')
    plt.scatter(data.index, data['Buy_Signal_price'], color='green', marker='^', alpha=1, label='Buy Signal')
    plt.scatter(data.index, data['Sell_Signal_price'], color='red', marker='v', alpha=1, label='Sell Signal')
    plt.title(symbol + ' Buy & Sell Signals')
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Close Price', fontsize=15)
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()


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

def backtest():
    while True:
        pass
        try:
            stop_if_stock_market_is_closed()
            load_stocks_list()
                       
            SYMBOLS = load_stocks_list()
            for symbol in SYMBOLS:
                data = get_data(stocks=symbol)
                df = pd.DataFrame(data['Adj Close']).rename(columns={'Adj Close': 'Close'})
                df['Open'] = data['Open']
                df['High'] = data['High']
                df['Low'] = data['Low']
                OCC_Strategy(df)

                if debug_mode:
                    plot_graph(df, symbol)

                for i in range(len(df)):
                    if not pd.isnull(df['Buy_Signal_price'][i]):
                        qty = check_cash(api, symbol)
                        if qty:
                            make_order(api, symbol, qty, 'buy')
                            log_order(symbol, 'Bought')

                            time.sleep(300)
                            print(" Waiting for 5 minutes after placing the most recent buy stock order to allow the ")
                            print(" account to update before placing more buy orders. ")
                            time.sleep(15)

                            remove_symbol(symbol, filename1)
                            SYMBOLS = load_stocks_list()

                            print("The buy stock order has been submitted. The stock symbol has been removed from "
                                  "successful-stocks-list.txt to finish the order process.")

                    elif not pd.isnull(df['Sell_Signal_price'][i]):
                        qty = get_position_qty(api, symbol)
                        if qty:
                            make_order(api, symbol, qty, 'sell')
                            log_order(symbol, 'Sold')



            time.sleep(2)  # Sleep for 1 minute and then check again


        except Exception as e:
            print(f'An error occurred: {e}')
            time.sleep(2)

if __name__ == "__main__":
    try:
        pass
        backtest()

    except KeyboardInterrupt:
        print('Interrupted by user')

    time.sleep(2)
