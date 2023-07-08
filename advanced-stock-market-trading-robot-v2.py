import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
from talib import MACD, RSI, BBANDS
from datetime import datetime, timedelta
from datetime import time as time2
import backtrader as bt
import os
import logging
import pytz
import time as time1
import sys

# Initialize the Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

eastern_zone = 'America/New_York'
current_time_zone = datetime.now(pytz.timezone(eastern_zone))

current_time = datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")

# Set up logging
logging.basicConfig(filename='stock_bot.log', level=logging.INFO, format='%(asctime)s %(message)s')


# Load stock symbols from a text file
def load_symbols(filename):
    symbols = []
    try:
        with open(filename, 'r') as file:
            symbols = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return symbols


# Stock symbols to monitor
SYMBOLS = load_symbols('successful-stocks-list.txt')


def get_current_time_zone():
    current_time_zone = datetime.now(pytz.timezone(eastern_zone))
    return current_time_zone


def get_current_time():
    current_time = datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")
    return current_time


def print_account_info():
    # Get account details
    account = api.get_account()

    # Print account information
    print("\nAccount Information:")
    print(f"{(current_time)}")
    #print(account)  uncomment to view more account details
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
        closing_price = float(position.prev_close_price)
        print(f"Symbol: {symbol}, Current Price: ${current_price:.2f}, Yesterday's Closing Price: ${closing_price:.2f}")
    print("--------------------")

    # Log current positions
    logging.info("\nCurrent Positions:")
    for position in positions:
        symbol = position.symbol
        current_price = float(position.current_price)
        closing_price = float(position.prev_close_price)
        logging.info(
            f"Symbol: {symbol}, Current Price: ${current_price:.2f}, Yesterday's Closing Price: ${closing_price:.2f}")
    logging.info("--------------------")


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        self.macd = bt.indicators.MACD(self.data.close)
        self.bbands = bt.indicators.BollingerBands(self.data.close)

    def next(self):
        if not self.position:
            # Buy condition
            if self.data.close[0] > self.data.close[
                -1] * 1.09 and self.rsi < 30 and self.macd.macd > self.macd.signal and self.data.close < self.bbands.lines.bot:
                cash = float(api.get_account().cash)
                symbol = self.data._name
                if not bearish(symbol):
                    self.buy_stock(symbol, cash)
        else:
            # Sell condition
            if self.data.close[0] < self.data.close[-1] * 0.975:
                self.sell_stock(self.position)


def backtest(strategy, data):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)
    cerebro.adddata(data)
    cerebro.run()


def bullish(symbol):
    # Download historical data
    bars = yf.download(symbol, period="1mo")
    close_prices = bars['Close']

    # Calculate MACD, RSI, and Bollinger Bands
    macd, _, _ = MACD(close_prices)
    rsi = RSI(close_prices)
    _, _, lower = BBANDS(close_prices)

    # Check bullish conditions
    macd_signal = macd[-1] > 0  # MACD is positive
    rsi_signal = rsi[-1] < 30  # RSI is below 30 (oversold)
    bollinger_signal = close_prices[-1] < lower[-1]  # Price is below lower Bollinger Band

    return macd_signal and rsi_signal and bollinger_signal


def bearish(symbol):
    # Download historical data
    bars = yf.download(symbol, period="1mo")
    close_prices = bars['Close']

    # Calculate MACD, RSI, and Bollinger Bands
    macd, _, _ = MACD(close_prices)
    rsi = RSI(close_prices)
    upper, _, _ = BBANDS(close_prices)

    # Check bearish conditions
    macd_signal = macd[-1] < 0  # MACD is negative
    rsi_signal = rsi[-1] > 70  # RSI is above 70 (overbought)
    bollinger_signal = close_prices[-1] > upper[-1]  # Price is above upper Bollinger Band

    return macd_signal and rsi_signal and bollinger_signal


def evaluate_stock(symbol):
    df = yf.download(symbol, period="6mo")
    df["RSI"] = RSI(df["Close"], timeperiod=14)
    df["MACD"], _, _ = MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["Upper Band"], df["Middle Band"], df["Lower Band"] = BBANDS(df["Close"], timeperiod=20)

    data = bt.feeds.PandasData(dataname=df)

    backtest(MyStrategy, data)

    # Calculate the percentage change from the initial value to the final value
    initial_value = df["Close"].iloc[0]
    final_value = df["Close"].iloc[-1]
    percent_change = (final_value - initial_value) / initial_value * 100

    # Calculate the percentage change between yesterday's closing price and the current price
    closing_price = df["Close"].iloc[-2]
    current_price = df["Close"].iloc[-1]
    price_change = (current_price - closing_price) / closing_price * 100

    # Print evaluation results with bullish/bearish indication
    print(f"Evaluation results for {symbol}:")
    print(f"Current Price: ${current_price:.2f}")
    print(f"Previous Opening Price: ${df['Open'].iloc[-1]:.2f}")
    print(f"Previous Closing Price: ${closing_price:.2f}")
    print(f"Percentage Change: {price_change:.2f}%")
    print(f"RSI: {df['RSI'].iloc[-1]:.2f}")
    print(f"MACD: {df['MACD'].iloc[-1]:.2f}")
    print(
        f"Bollinger Bands: {df['Upper Band'].iloc[-1]:.2f} - {df['Middle Band'].iloc[-1]:.2f} - {df['Lower Band'].iloc[-1]:.2f}")
    print(f"6-Month Percentage Change to identify Bullish or Bearish stocks: {percent_change:.2f}%")
    print(f"Bullish: {bullish(symbol)}")
    print(f"Bearish: {bearish(symbol)}")
    print("--------------------")

    # Log evaluation results with bullish/bearish indication
    logging.info(f"Evaluation results for {symbol}:")
    logging.info(f"Current Price: ${current_price:.2f}")
    logging.info(f"Previous Opening Price: ${df['Open'].iloc[-1]:.2f}")
    logging.info(f"Previous Closing Price: ${closing_price:.2f}")
    logging.info(f"Percentage Change: {price_change:.2f}%")
    logging.info(f"RSI: {df['RSI'].iloc[-1]:.2f}")
    logging.info(f"MACD: {df['MACD'].iloc[-1]:.2f}")
    logging.info(
        f"Bollinger Bands: {df['Upper Band'].iloc[-1]:.2f} - {df['Middle Band'].iloc[-1]:.2f} - {df['Lower Band'].iloc[-1]:.2f}")
    logging.info(f"6-Month Percentage Change to identify Bullish or Bearish stocks: {percent_change:.2f}%")
    logging.info(f"Bullish: {bullish(symbol)}")
    logging.info(f"Bearish: {bearish(symbol)}")
    logging.info("--------------------")


def buy_stock(symbol, cash):
    # Get account and check day trade count
    account = api.get_account()
    if account.daytrade_count > 2:
        print("Day trade limit reached. Not buying.")
        return

    # Prevent buying if stock is bearish
    if bearish(symbol):
        print(f"The stock {symbol} is bearish. Not buying.")
        return

    # Get the last closing price of the stock
    bars = yf.download(symbol, period="1d")
    price = bars['Close'].iloc[-1]

    # Calculate the maximum number of shares we can buy
    num_shares = int(cash / price)

    # If we can't buy at least 1 share, then don't submit the order
    if num_shares < 1:
        print(f"Not enough cash to buy a single share of {symbol}")
        return

    # Submit the order
    api.submit_order(
        symbol=symbol,
        qty=num_shares,
        side='buy',
        type='market',
        time_in_force='day'
    )
    print(f"Submitted order to buy {num_shares} shares of {symbol}")


def sell_stock(self, position):
    # Get account and check day trade count
    account = api.get_account()
    if account.daytrade_count > 3:
        print("Day trade limit reached. Not selling.")
        return

    if position.qty > 0:
        # Submit an order to sell all shares of this stock
        api.submit_order(
            symbol=position.symbol,
            qty=position.qty,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"Submitted order to sell all shares of {position.symbol}")


def sell_dropped_stocks():
    # Get current positions
    positions = api.list_positions()
    account = api.get_account()

    for position in positions:
        # Get the current price from the Position object
        current_price = float(position.current_price)

        # Check for 2.5% price decrease and sell
        if float(position.avg_entry_price) * 0.975 > current_price:
            # Check if there is at least 1 share to sell
            if int(position.qty) > 0 and account.daytrade_count < 3:
                api.submit_order(
                    symbol=position.symbol,
                    qty=position.qty,
                    side='sell',
                    type='market',
                    time_in_force='day'
                )


def sell_profitable_positions():
    # Get current positions
    positions = api.list_positions()
    account = api.get_account()

    for position in positions:
        # Get the current price from the Position object
        current_price = float(position.current_price)
        entry_price = float(position.avg_entry_price)

        # Calculate the percentage change
        percent_change = (current_price - entry_price) / entry_price * 100

        # Sell if the price increases by 3% and we own more than 0 shares
        if percent_change >= 3.0 and int(position.qty) > 0 and account.daytrade_count < 3:
            api.submit_order(
                symbol=position.symbol,
                qty=position.qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
            print(f"Sold {position.qty} shares of {position.symbol} with a {percent_change:.2f}% profit.")

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
         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %H:%M:%S")}\n')
        print("Stockbot only works Monday through Friday: 9:30am - 4:00pm Eastern Time. ")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program. ")
        time1.sleep(60)  # Sleep for 1 minute and check again
        #return

def check_account_status():
    account = api.get_account()
    if account.trading_blocked:
        print('Account is currently restricted from trading.')
        time1.sleep(60 * 60 * 24)
        sys.exit(0)

def monitor_stocks():
    while True:
        stop_if_stock_market_is_closed()

        check_account_status()

        # earn money on selling stocks
        sell_profitable_positions()

        sell_dropped_stocks()

        # Print account information
        print_account_info()

        # Print current positions
        print_positions()

        # Evaluate and print monitored stocks
        for symbol in SYMBOLS:
            evaluate_stock(symbol)

        # Sleep for 1 minute before checking again
        time1.sleep(60)


if __name__ == "__main__":
    while True:
        try:
            monitor_stocks()
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")
            # Sleep for 5 seconds before restarting the program
            time1.sleep(5)
            continue
