import os
import logging
import alpaca_trade_api as tradeapi
from datetime import timedelta
import datetime
import yfinance as yf
from typing import List, Dict
import time as time1
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
from matplotlib.pyplot import style
import numpy as np
import pytz

style.use('fivethirtyeight')

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# Initialize global variables
global TimeFrame, startdate, end_date

eastern_zone = 'America/New_York'
current_time_zone = datetime.datetime.now(pytz.timezone(eastern_zone))


def get_symbol_data_yf(symbol):
    # Get today's date
    today = datetime.datetime.today()

    # Calculate the date 30 days ago
    one_year_ago = today - timedelta(days=364)

    # Format dates
    today_str = today.strftime('%Y-%m-%d')
    one_year_ago_ago_str = one_year_ago.strftime('%Y-%m-%d')

    # Download data
    data = yf.download(symbol, start=one_year_ago_ago_str, end=today_str)

    return data


# Load stock symbols from a text file
def load_symbols(filename: str) -> List[str]:
    symbols = []
    try:
        with open(filename, 'r') as file:
            symbols = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return symbols


# Stock symbols to monitor
SYMBOLS = load_symbols('successful-stocks-list.txt')

# MACD Indicator parameters
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
RISK = 0.025


def api_request_limiter(func):
    """
    Decorator function to limit the number of requests to Alpaca API
    """

    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        time1.sleep(0.3)  # Sleep for 300 milliseconds
        return response

    return wrapper


# Alpaca API functions
@api_request_limiter
def get_position(symbol: str):
    try:
        return api.get_position(symbol)
    except Exception as e:
        return None


@api_request_limiter
def get_asset(symbol: str):
    return api.get_asset(symbol)


@api_request_limiter
def list_orders():
    return api.list_orders()


@api_request_limiter
def submit_order(symbol: str, qty: int, side: str, type: str, time_in_force: str):
    return api.submit_order(symbol, qty, side, type, time_in_force)


@api_request_limiter
def get_account():
    return api.get_account()


@api_request_limiter
def cancel_order(order_id: str):
    return api.cancel_order(order_id)


@api_request_limiter
def get_last_trade(symbol: str):
    return api.get_last_trade(symbol)


def evaluate_and_trade(symbol, data, account):
    last_row = data.iloc[-1]

    # MACD strategy
    macd = ta.macd(data['Close'], fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL)
    data = pd.concat([data, macd], axis=1).reindex(data.index)
    MACD_Strategy(data, RISK)

    # If MACD strategy indicates a buy signal and we have enough cash
    if not np.isnan(last_row['MACD_Buy_Signal_price']) and float(account.cash) > last_row['MACD_Buy_Signal_price']:
        qty = int(float(account.cash) / last_row['MACD_Buy_Signal_price'])
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc',
        )
        print(f'Bought {qty} shares of {symbol}')

    # If MACD strategy indicates a sell signal and we own the stock
    positions = api.list_positions()
    position_symbols = [position.symbol for position in positions]
    if not np.isnan(last_row['MACD_Sell_Signal_price']) and symbol in position_symbols:
        qty = [position.qty for position in positions if position.symbol == symbol][0]
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc',
        )
        print(f'Sold {qty} shares of {symbol}')


# MACD Strategy
def MACD_Strategy(df: pd.DataFrame, risk: float) -> Dict[str, List[float]]:
    MACD_Buy = []
    MACD_Sell = []
    position = False

    for i in range(0, len(df)):
        if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i]:
            MACD_Sell.append(np.nan)  # This is the NaN sell signal
            if position == False:
                MACD_Buy.append(df['Adj Close'][i])
                position = True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i]:
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(df['Adj Close'][i])  # This is the NaN buy signal
                position = False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and df['Adj Close'][i] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(df["Adj Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and df['Adj Close'][i] < df['Adj Close'][i - 1] * (1 - risk):
            MACD_Sell.append(df["Adj Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    return {'MACD_Buy_Signal_price': MACD_Buy, 'MACD_Sell_Signal_price': MACD_Sell}


# MACD Color Function
def MACD_color(data: pd.DataFrame) -> List[bool]:
    MACD_color = []
    for i in range(0, len(data)):
        if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color


# Debug and Plot function
def debug_and_plot(data: pd.DataFrame, symbol: str, plot: bool = False):
    # Update Data
    MACD_strategy = MACD_Strategy(data, RISK)
    data = data.assign(MACD_Buy_Signal_price=MACD_strategy['MACD_Buy_Signal_price'])
    data = data.assign(MACD_Sell_Signal_price=MACD_strategy['MACD_Sell_Signal_price'])
    data['positive'] = MACD_color(data)

    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.suptitle(symbol, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot('Adj Close', data=data, label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)

    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index, 'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),
            width=1, alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()
    if plot:
        plt.show()


def get_current_time_zone():
    current_time_zone = datetime.datetime.now(pytz.timezone(eastern_zone))
    return current_time_zone


def get_current_time():
    current_time = datetime.datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")
    return current_time


def print_account_info():
    current_time = datetime.datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")
    # Get account details
    account = api.get_account()

    # Print account information
    print("\nAccount Information:")
    print(f" Eastern Time Zone: {(current_time)}")
    # print(account)  uncomment to view more account details
    print(f"Day Trade Count: {account.daytrade_count} out of 3 total Day Trades in 5 business days.")
    print(f"Current Account Cash: ${float(account.cash):.2f}")
    print("--------------------")

    # Log account information
    logging.info("\nAccount Information:")
    logging.info(f"{get_current_time()}")
    logging.info(f"Day Trade Count: {account.daytrade_count} out of 3 total Day Trades in 5 business days.")
    logging.info(f"Current Account Cash: ${float(account.cash):.2f}")
    logging.info("--------------------")


def print_positions():
    # Get current positions
    positions = api.list_positions()

    # Print current positions
    print("\nCurrent Positions:")
    for position in positions:
        symbol = position.symbol
        current_price = float(position.current_price)
        print(f"Symbol: {symbol}, Current Price: ${current_price:.2f}")
        print("--------------------")

    # Log current positions
    logging.info("\nCurrent Positions:")
    for position in positions:
        symbol = position.symbol
        current_price = float(position.current_price)
        logging.info(
            f"Symbol: {symbol}, Current Price: ${current_price:.2f}")
    logging.info("--------------------")


def monitor_stocks():
    # Load account information
    account = api.get_account()
    # Initial sleep offset
    time1.sleep(2)

    while True:
        try:
            # Refresh account information and daytrades count
            account = api.get_account()
            daytrades = account.daytrade_count

            print_account_info()
            print_positions()

            # Get market clock
            clock = api.get_clock()

            # Open the market
            #if clock.is_open and int(account.daytrade_count) < 3:
            symbols = SYMBOLS
            for symbol in symbols:
                data = get_symbol_data_yf(symbol)
                evaluate_and_trade(symbol, data, account)
                debug_and_plot(data, symbol)

            #else:
                # Get the current time in Eastern Time
                eastern = pytz.timezone('US/Eastern')
                now = datetime.datetime.now(eastern)
                current_time = now.time()

                # Close the market
                print('''

                           _____   __                   __             ____            __            __ 
                          / ___/  / /_  ____   _____   / /__          / __ \  ____    / /_   ____   / /_
                          \__ \  / __/ / __ \ / ___/  / //_/         / /_/ / / __ \  / __ \ / __ \ / __/
                         ___/ / / /_  / /_/ // /__   / ,<           / _, _/ / /_/ / / /_/ // /_/ // /_  
                        /____/  \__/  \____/ \___/  /_/|_|         /_/ |_|  \____/ /_.___/ \____/ \__/

                                  2023          https://github.com/CodeProSpecialist    

                         ''')
                print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %H:%M:%S")}\n')
                print("Stockbot only works Monday through Friday: 9:30am - 4:00pm Eastern Time. ")
                print("Waiting until Stock Market Hours to begin the Stockbot Trading Program. ")
                print('________________________________________________________')
                print('The Stock Market is closed or our daytrade count is 3.')
                print(' Please return when your daytrade count is 1 or 2  ')
                print(' and when the Stock Market is Open. ')
                # Calculate time until open and sleep
                time_to_open = clock.next_open - clock.timestamp
                print(f'Sleeping for {time_to_open.total_seconds()} seconds')
                #time1.sleep(time_to_open.total_seconds())
        except Exception as e:
            print(str(e))
        time1.sleep(2)


if __name__ == '__main__':
    while True:
        try:
            monitor_stocks()

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")
            # Sleep for 2 seconds before restarting the program
            time1.sleep(2)
            continue
