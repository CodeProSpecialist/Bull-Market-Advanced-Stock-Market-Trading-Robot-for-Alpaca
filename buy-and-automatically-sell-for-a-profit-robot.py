import os
import time
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import alpaca_trade_api as tradeapi
import pytz
from datetime import datetime
from datetime import time as time2
import matplotlib.pyplot as plt
import numpy as np

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
debug_mode = False


def load_stocks_list():
    with open('successful-stocks-list.txt', 'r') as file:
        return [line.strip() for line in file]


def get_data(symbol):
    return yf.download(symbol, period='1d', interval='1m')


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
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell


def MACD_color(df):
    MACD_color = []
    for i in range(0, len(df)):
        if df['MACDh_12_26_9'][i] > df['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color


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


def plot_macd_graph(data, symbol):
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
                    2023                 https://github.com/CodeProSpecialist
        
         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %H:%M:%S")}\n')
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        time.sleep(60)  # Sleep for 1 minute and check again



def main():
    stop_if_stock_market_is_closed()
    stocks_list = load_stocks_list()
    while True:
        try:
            print(f' Eastern Time: {datetime.now(eastern).strftime("%A, %B %d, %Y %I:%M:%S %p")}')
            positions = api.list_positions()
            if positions:
                print("Stocks in our Portfolio:")
                for position in positions:
                    print(f'{position.symbol}, Current Price: {round(float(position.current_price), 2)}')

                    if debug_mode:
                        data = get_data(position.symbol)
                        macd = ta.macd(data['Close'])
                        data = pd.concat([data, macd], axis=1).reindex(data.index)
                        MACD_Strategy(data, 0.025)
                        data['positive'] = MACD_color(data)
                        plot_macd_graph(data, position.symbol)  # plot the graph for owned stocks
            else:
                print("No stocks are currently in the portfolio.")

            print("Stocks to buy:")
            for symbol in stocks_list:
                data = get_data(symbol)
                current_price = round(data['Close'].iloc[-1], 2)  # rounding off to 2 decimal places
                print(f'{symbol}, Current Price: {current_price}')

                macd = ta.macd(data['Close'])
                data = pd.concat([data, macd], axis=1).reindex(data.index)
                MACD_Strategy(data, 0.025)
                data['positive'] = MACD_color(data)

                if debug_mode:
                    plot_macd_graph(data, symbol)  # Call the function to plot the graph

                account = api.get_account()
                daytrade_count = account.daytrade_count
                print(f'Total number of day trades out of 3 Maximum in 5 business days: {daytrade_count}')

                if data['MACD_Buy_Signal_price'].iloc[-1] > 0 and int(daytrade_count) < 3:
                    qty = check_cash(api, symbol)
                    if qty:
                        make_order(api, symbol, qty, 'buy')
                        log_order(symbol, 'buy')
                        time.sleep(600)

                elif data['MACD_Sell_Signal_price'].iloc[-1] > 0:
                    qty = get_position_qty(api, symbol)
                    if qty:
                        make_order(api, symbol, qty, 'sell')
                        log_order(symbol, 'sell')
            time.sleep(2)
        except Exception as e:
            print(f'An error occurred: {e}')
            time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by user')
    except Exception as e:
        print('Error:', e)
        time.sleep(2)
        main()
