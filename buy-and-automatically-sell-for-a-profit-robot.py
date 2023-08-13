import os
import time
import pandas as pd
import yfinance as yf
import pandas_ta as ta
#import pandas_datareader.data as web
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

global risk, symbol, data, SYMBOLS

risk = 0.025

filename1 = 'successful-stocks-list.txt'


def load_stocks_list():
    with open('successful-stocks-list.txt', 'r') as file:
        return [line.strip() for line in file]


SYMBOLS = []
end_date = date.today()
startdate = end_date - timedelta(days=180)
print(end_date)


def get_data(stocks=SYMBOLS, start=startdate, end=end_date, debug=False):
    data = yf.download(stocks, start=start, end=end)

    # Check for any missing values and handle them
    if data.isnull().any().any():
        print("Missing values detected, applying forward-fill.")
        data.fillna(method='ffill', inplace=True)

    # If you still have missing values (e.g., at the beginning of the DataFrame),
    # you might choose to drop those rows
    data.dropna(inplace=True)

    if debug:
        print("Downloaded data shape:", data.shape)
        print("Downloaded data columns:", data.columns)
        print("First few rows of data:")
        print(data.head())

    return data


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

def MACD_Strategy(df, risk):
    MACD_Buy = [np.nan] * len(df)
    MACD_Sell = [np.nan] * len(df)
    position = False

    for i in range(0, len(df)):
        if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i]:
            MACD_Sell.append(np.nan)
            if position ==False:
                MACD_Buy.append(df['Adj Close'][i])
                position=True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i]:
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(df['Adj Close'][i])
                position=False
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

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell

def MACD_color(data):
    MACD_color = []
    for i in range(0, len(data)):
        if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color


def compute_zema(series, length=22):
    ema1 = series.ewm(span=length).mean()
    ema2 = ema1.ewm(span=length).mean()
    zema_val = ema1 + (ema1 - ema2)
    return zema_val


def OCC_Strategy(df):
    occ_signal_buy = [np.nan]
    occ_signal_sell = [np.nan]
    position = False

    atr = ta.atr(df.High, df.Low, df.Close, length=22)
    zema_val = compute_zema(df.Close)
    upper = zema_val + (atr * 3)
    lower = zema_val - (atr * 0.6)

    buffer = atr * 1.5
    upper_buffer = zema_val + buffer
    lower_buffer = zema_val - buffer

    macd_line, signal_line, _ = ta.macd(df.Close)

    for i in range(len(df)):
        if (df['Close'][i] > upper[i] and not position and 
            (i == 0 or (macd_line[i] > signal_line[i] and macd_line[i-1] <= signal_line[i-1]))):
            occ_signal_buy.append(df['Close'][i])
            occ_signal_sell.append(np.nan)
            position = True
        elif (df['Close'][i] < lower_buffer[i] and position and 
              (i == 0 or (macd_line[i] < signal_line[i] and macd_line[i-1] >= signal_line[i-1]))):
            occ_signal_buy.append(np.nan)
            occ_signal_sell.append(df['Close'][i])
            position = False
        else:
            occ_signal_buy.append(np.nan)
            occ_signal_sell.append(np.nan)

    df['Buy_Signal_price'] = occ_signal_buy
    df['Sell_Signal_price'] = occ_signal_sell
    df['Zema'] = zema_val
    df['Upper'] = upper
    df['Lower'] = lower
    df['Upper_Buffer'] = upper_buffer
    df['Lower_Buffer'] = lower_buffer

    return df


def plot_graph(data, symbol):
    global macd
    macd = ta.macd(data['Close'])
    data = pd.concat([data, macd], axis=1).reindex(data.index)
    MACD_Strategy(data, 0.025)
    data['positive'] = MACD_color(data)
    OCC_Strategy(data)

    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(symbol, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot('Adj Close',data=data, label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)

    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index,'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),width=1,alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()
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

            if current_price <= purchase_price * 0.99: # 1.0% decrease
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
            global SYMBOLS  # Declare SYMBOLS as a global variable
            stocks_list = load_stocks_list()

            print(f' Eastern Time: {datetime.now(eastern).strftime("%A, %B %d, %Y %I:%M:%S %p")}')

            sell_decreasing_stocks(api)

            positions = api.list_positions()

            if positions:
                print("Stocks in our Portfolio:")
                for position in positions:
                    print(f'{position.symbol}, Current Price: {round(float(position.current_price), 2)}')
            else:
                print("No stocks are in our portfolio..... not looking to sell stocks right now.")


            print("Stocks to buy:")
            for symbol in SYMBOLS:  # I assume you meant SYMBOLS which is your stocks_list
                #data = get_data(symbol)
                data = get_data(stocks=[symbol])
                if not data.empty:
                    current_price = round(data['Close'].iloc[-1], 2)
                else:
                    print(f"No data available for {symbol}. Skipping...")
                    continue

                current_price = round(data['Close'].iloc[-1], 2)  # rounding off to 2 decimal places
                print(f'{symbol}, Current Price: {current_price}')


            SYMBOLS = load_stocks_list()
            for symbol in SYMBOLS:
                #data = get_data(stocks=symbol)
                data = get_data(stocks=[symbol])
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
