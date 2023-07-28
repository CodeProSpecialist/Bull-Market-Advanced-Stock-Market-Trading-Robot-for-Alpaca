import alpaca_trade_api as tradeapi
import pandas as pd
import tradingview_ta as ta
import yfinance as yf
from talib import MACD, RSI, BBANDS, ATR  # Import ATR from talib
from datetime import datetime
from datetime import time as time2
import os
import logging
import pytz
import time
import sys

# Initialize the Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

eastern_zone = 'America/New_York'
current_time_zone = datetime.now(pytz.timezone(eastern_zone))

global current_time
global symbols, SYMBOLS

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
    current_time = datetime.now(pytz.timezone(eastern_zone)).strftime("%A, %b-%d-%Y %H:%M:%S")
    # Get account details
    account = api.get_account()

    # Print account information
    print("\nAccount Information:")
    print(f"{(current_time)}")
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


def get_opening_price(symbol):
    # Fetch the opening price of today
    bars = yf.download(symbol, period="1d")
    opening_price = bars["Open"].iloc[0]
    return opening_price


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


# Function to get current positions using Alpaca API
def get_positions(api):
    positions = api.list_positions()
    return positions

def evaluate_owned_shares_and_generate_sell_signal_at_high_bollinger_band(api):
    # Get current positions
    positions = get_positions(api)

    # Loop through the positions and evaluate each stock
    for position in positions:
        symbol = position.symbol

        # Get stock data and calculate indicators
        df = yf.download(symbol, period="6mo")
        df["RSI"] = RSI(df["Close"], timeperiod=14)
        df["MACD"], _, _ = MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
        df["Upper Band"], df["Middle Band"], df["Lower Band"] = BBANDS(df["Close"], timeperiod=20)

        # Calculate the percentage change from the initial value to the final value
        initial_value = df["Close"].iloc[0]
        final_value = df["Close"].iloc[-1]
        percent_change = (final_value - initial_value) / initial_value * 100

        # Calculate the percentage change between yesterday's closing price and the current price
        closing_price = df["Close"].iloc[-2]
        current_price = df["Close"].iloc[-1]
        price_change = (current_price - closing_price) / closing_price * 100

        # Sell stock if it reaches the upper Bollinger Band
        if current_price >= df["Upper Band"].iloc[-1]:
            sell_stock(position)

        # Print evaluation results with bullish/bearish indication
        print(f"Evaluation results for {symbol}:")
        print(f"Current Price: ${current_price:.2f}")
        print(f"Previous Opening Price: ${df['Open'].iloc[-1]:.2f}")
        print(f"Previous Closing Price: ${closing_price:.2f}")
        print(f"Percentage Change: {price_change:.2f}%")
        print(f"RSI: {df['RSI'].iloc[-1]:.2f}")
        print(f"MACD: {df['MACD'].iloc[-1]:.2f}")
        print(f"Bollinger Bands: {df['Upper Band'].iloc[-1]:.2f} - {df['Middle Band'].iloc[-1]:.2f} - {df['Lower Band'].iloc[-1]:.2f}")
        print(f"6-Month Percentage Change to identify Bullish or Bearish stocks: {percent_change:.2f}%")
        print(f"Waiting to Sell all Shares of {symbol} for a profit when the price reaches the Upper Bollinger Band. ")
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
        logging.info(f"Bollinger Bands: {df['Upper Band'].iloc[-1]:.2f} - {df['Middle Band'].iloc[-1]:.2f} - {df['Lower Band'].iloc[-1]:.2f}")
        logging.info(f"6-Month Percentage Change to identify Bullish or Bearish stocks: {percent_change:.2f}%")
        logging.info(f"Waiting to Sell all Shares of {symbol} for a profit when the price reaches the Upper Bollinger Band. ")
        logging.info(f"Bullish: {bullish(symbol)}")
        logging.info(f"Bearish: {bearish(symbol)}")
        logging.info("--------------------")


def evaluate_stock(symbol):
    df = yf.download(symbol, period="6mo")
    df["RSI"] = RSI(df["Close"], timeperiod=14)
    df["MACD"], _, _ = MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["Upper Band"], df["Middle Band"], df["Lower Band"] = BBANDS(df["Close"], timeperiod=20)

    # Calculate the percentage change from the initial value to the final value
    initial_value = df["Close"].iloc[0]
    final_value = df["Close"].iloc[-1]
    percent_change = (final_value - initial_value) / initial_value * 100

    # Calculate the percentage change between yesterday's closing price and the current price
    closing_price = df["Close"].iloc[-2]
    current_price = df["Close"].iloc[-1]
    price_change = (current_price - closing_price) / closing_price * 100

    # buy stock in your text file of successful stocks when the price decreases 3% 
    # to get a profit when the stock price will increase in the future. 
    if price_change < 3:
        account = api.get_account()
        cash = float(account.cash)
        buy_stock(symbol, cash)

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


# the python code below will remove the stock from the text file after the buy order is placed
def remove_symbol(symbol, filename):
    symbols = []
    try:
        with open(filename, 'r') as file:
            symbols = [line.strip() for line in file.readlines() if line.strip() != symbol]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    with open(filename, 'w') as file:
        for s in symbols:
            file.write(s + "\n")

    # Clear the 'symbols' and 'SYMBOLS' variables
    SYMBOLS = load_symbols(filename)

    symbols.clear()
    SYMBOLS.clear()

    # Update the 'symbols' and 'SYMBOLS' variables with new information
    symbols = load_symbols(filename)
    SYMBOLS = load_symbols(filename)


def buy_stock(symbol, cash):
    df = yf.download(symbol, period="6mo")
    df["RSI"] = RSI(df["Close"], timeperiod=14)
    df["MACD"], _, _ = MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
    df["Upper Band"], df["Middle Band"], df["Lower Band"] = BBANDS(df["Close"], timeperiod=20)

    # Calculate the percentage change from the initial value to the final value
    initial_value = df["Close"].iloc[0]
    final_value = df["Close"].iloc[-1]
    percent_change = (final_value - initial_value) / initial_value * 100

    # Get account and check day trade count
    account = api.get_account()
    if account.daytrade_count >= 3:
        print(" Day trade limit would be reached if we tried to sell after buying today. "
              " Not buying until Day Trade number is 2 or less. ")
        logging.info("Day trade limit would be reached if we tried to sell after buying today. "
                     " Not buying until Day Trade number is 2 or less. ")
        return

    # Prevent buying if stock is bearish
    if bearish(symbol):
        print(f"The stock {symbol} is bearish. Not buying.")
        logging.info(f"The stock {symbol} is bearish. Not buying.")
        return

    # A second important check to not buy if stock is bearish to prevent loss of profit
    # Check if the 6 month percent change is less than 25%, to not buy bearish stocks
    if percent_change < 25:
        print(f"The percent change for {symbol} is less than 25% for 6 months. Not buying bearish stock. ")
        logging.info(f"The percent change for {symbol} is less than 25% for 6 months. Not buying bearish stock. ")
        return

    # Get the last closing price of the stock
    bars = yf.download(symbol, period="1d")
    price = bars['Close'].iloc[-1]

    # Calculate the maximum number of shares we can buy
    num_shares = int(cash / price)

    # If we can't buy at least 1 share, then don't submit the order
    if num_shares < 1:
        print(f"Not enough cash to buy a single share of {symbol}")
        logging.info(f"Not enough cash to buy a single share of {symbol}")
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
    logging.info(f"Submitted order to buy {num_shares} shares of {symbol}")

    time.sleep(15)  # waiting 15 seconds to remove the stock from the text file

    # remove the symbol from the list file after successful order
    remove_symbol(symbol, 'successful-stocks-list.txt')

    global symbols

    # Clear the 'symbols' and 'SYMBOLS' variables

    SYMBOLS = load_symbols('successful-stocks-list.txt')

    symbols.clear()
    SYMBOLS.clear()

    # Update the 'symbols' and 'SYMBOLS' variables with new information
    symbols = load_symbols('successful-stocks-list.txt')
    SYMBOLS = load_symbols('successful-stocks-list.txt')

    print("The buy stock order has been submitted. The stock symbol has been removed from successful-stocks-list.txt to finish the order process.")
    logging.info("The buy stock order has been submitted. The stock symbol has been removed from successful-stocks-list.txt to finish the order process.")

    print("Waiting 10 minutes for the order to 100% finish updating in the account. ")
    logging.info("Waiting 10 minutes for the order to 100% finish updating in the account. ")
    time.sleep(600)  # wait 10 minutes for the order to 100% finish updating in the account.


def sell_stock(position):
    # Get account and check day trade count
    account = api.get_account()
    if account.daytrade_count >= 3:
        print("Day trade limit reached. Not selling.")
        logging.info("Day trade limit reached. Not selling.")
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
        logging.info(f"Submitted order to sell all shares of {position.symbol}")
        print("Waiting 10 minutes for the order to 100% finish updating in the account. ")
        logging.info("Waiting 10 minutes for the order to 100% finish updating in the account. ")
        time.sleep(600)  # wait 10 minutes for the order to 100% finish updating in the account.


def get_rsi(data, period=14):
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def sell_dropped_stocks():
    # Get current positions
    account = api.get_account()
    positions = api.list_positions()

    for position in positions:
        # Get historical price data
        symbol = position.symbol
        historical_data = yf.download(symbol, period="7d")  # Download data for the last 7 days
        current_price = float(position.current_price)

        # Variables for trailing stop loss
        highest_price = float(position.avg_entry_price)  # Initialize highest price
        stop_loss_percentage = 0.10  # Set stop loss percentage to 10%
        stop_loss_price = highest_price * (1 - stop_loss_percentage)  # Calculate stop loss price
        stop_loss_triggered = False

        # Variables for consecutive price decreases
        consecutive_decreases = 0
        previous_price = current_price

        # Check if the price meets the sell conditions
        if current_price < float(position.avg_entry_price) - 0.52 or consecutive_decreases >= 2:
            # Calculate RSI
            rsi = get_rsi(historical_data['Close'])

            # Additional sell conditions
            if rsi.iloc[-1] < 30 and rsi.iloc[-2] > rsi.iloc[-1]:
                # Sell the stock
                # Add your code here to execute the sell operation
                if float(position.qty) > 0 and account.daytrade_count < 3:
                    api.submit_order(
                        symbol=position.symbol,
                        qty=float(position.qty),
                        side='sell',
                        type='market',
                        time_in_force='day'
                    )
                    print(f"Submitted order to sell all shares of {position.symbol}")
                    logging.info(f"Submitted order to sell all shares of {position.symbol}")
                    print("Waiting 10 minutes for the order to 100% finish updating in the account.")
                    logging.info("Waiting 10 minutes for the order to 100% finish updating in the account.")
                    time.sleep(600)  # wait 10 minutes for the order to 100% finish updating in the account.

        # Update trailing stop loss and consecutive price decreases
        if current_price > highest_price:
            highest_price = current_price
            stop_loss_price = highest_price * (1 - stop_loss_percentage)
            consecutive_decreases = 0
        else:
            if current_price < previous_price:
                consecutive_decreases += 1
            else:
                consecutive_decreases = 0

        # Check if stop loss is triggered
        if current_price < stop_loss_price:
            stop_loss_triggered = True

        # Update previous price for the next iteration
        previous_price = current_price

        # Wait for 2 seconds before repeating the process
        time.sleep(2)


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

                  2023          https://github.com/CodeProSpecialist    
        
         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %H:%M:%S")}\n')
        print("Stockbot only works Monday through Friday: 9:30am - 4:00pm Eastern Time. ")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program. ")
        time.sleep(60)  # Sleep for 1 minute and check again
        # return


def check_account_status():
    account = api.get_account()
    if account.trading_blocked:
        print('Account is currently restricted from trading.')
        time.sleep(60 * 60 * 24)
        sys.exit(0)


def monitor_stocks():
    while True:
        pass
        stop_if_stock_market_is_closed()

        check_account_status()

        sell_dropped_stocks()

        # Print account information
        print_account_info()

        # Print current positions
        print_positions()

        # Loop through the list of symbols
        for symbol in SYMBOLS:
            try:
                # Fetch historical price data for the symbol with 1-minute interval
                df = yf.download(symbol, period="1d", interval="1m")

                # Call the function for the specific symbol
                evaluate_owned_shares_and_generate_sell_signal_at_high_bollinger_band(api)

                # Evaluate and print monitored stocks
                evaluate_stock(symbol)

            except Exception as e:
                print(f"Error processing {symbol}: {e} in the monitor_stocks Python code section. ")
                print("It is OK to ignore the Error processing : No objects to concatenate message ")
                print("because it reports an Error when it reached the end of the text file list of successful stocks to buy. ")
                logging.error(f"Error processing {symbol}: {e} in the monitor_stocks Python code section. ")
                logging.error("It is OK to ignore the Error processing : No objects to concatenate message ")
                logging.error("because it reports an Error when it reached the end of the text file list of successful stocks to buy. ")
                continue

        time.sleep(2)


if __name__ == "__main__":
    while True:
        try:
            monitor_stocks()

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")
            # Sleep for 2 seconds before restarting the program
            time.sleep(2)
            continue

