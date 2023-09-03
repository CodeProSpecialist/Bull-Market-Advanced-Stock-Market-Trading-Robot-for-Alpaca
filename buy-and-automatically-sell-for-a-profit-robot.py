import threading
import logging
import os, sys
import time
from datetime import datetime
from datetime import time as time2
import alpaca_trade_api as tradeapi
import pytz
import talib
import yfinance as yf
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

PRINT_DATABASE = True  # keep this as True to view the stocks to sell.

DEBUG = False  # this robot works faster when this is False.

eastern = pytz.timezone('US/Eastern')

# Dictionary to maintain previous prices and price increase and price decrease counts
stock_data = {}

global stocks_to_buy

# the below variable was recommended by Artificial Intelligence
buy_sell_lock = threading.Lock()

logging.basicConfig(filename='log-file-of-buy-and-sell-signals.txt', level=logging.INFO)

# Define the Database Models
# Newer Data Base Model code below
Base = sqlalchemy.orm.declarative_base()


class TradeHistory(Base):
    __tablename__ = 'trade_history'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    action = Column(String)  # 'buy' or 'sell'
    quantity = Column(Integer)
    price = Column(Float)
    date = Column(DateTime)


class Position(Base):
    __tablename__ = 'positions'
    symbol = Column(String, primary_key=True)
    quantity = Column(Integer)
    avg_price = Column(Float)
    purchase_date = Column(DateTime)


# Initialize SQLAlchemy
engine = create_engine('sqlite:///trading_bot.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if not exist
Base.metadata.create_all(engine)


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
        
            2023 Edition of the Advanced Stock Market Trading Robot, Version 2 
           _____   __                   __             ____            __            __ 
          / ___/  / /_  ____   _____   / /__          / __ \  ____    / /_   ____   / /_
          \__ \  / __/ / __ \ / ___/  / //_/         / /_/ / / __ \  / __ \ / __ \ / __/
         ___/ / / /_  / /_/ // /__   / ,<           / _, _/ / /_/ / / /_/ // /_/ // /_  
        /____/  \__/  \____/ \___/  /_/|_|         /_/ |_|  \____/ /_.___/ \____/ \__/  

                                                  https://github.com/CodeProSpecialist

                       Featuring an An Accelerated Database Engine with Python 3 SQLAlchemy  

         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %I:%M:%S %p")}\n')
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        print("                                                                       ")
        print("This program will only work correctly if there is at least 1 stock symbol ")
        print("in the file named electricity-or-utility-stocks-to-buy-list.txt ")
        print("                                                                       ")
        print("The Stock Market Robot requires that you own at least 1 share or a fractional share of stock ")
        print("before you run the Stock Market Robot to allow the database to not be empty ")
        print("because the database can not be created when it is completely empty. ")
        print("A database needs to be created when this Stock Market Robot begins working ")
        print("to keep track of all of the stock position buying and selling. ")
        print("Thanks for understanding. Stocks can be purchased at the Alpaca website. ")
        print("This software is not affiliated or endorsed by Alpaca Securities, LLC ")
        print("This software does, however, try to be a useful, profitable, and valuable ")
        print("stock market trading application. ")
        time.sleep(60)  # Sleep for 1 minute and check again


def print_database_tables():
    if PRINT_DATABASE:
        # Print TradeHistory table
        print("\nTrade History In This Robot's Database:")
        print("\n")
        print("Stock | Buy or Sell | Quantity | Avg. Price | Purchase Date ")
        print("\n")

        for record in session.query(TradeHistory).all():
            print(record.symbol, record.action, record.quantity, record.price, record.date)

        print("----------------------------------------------------------------")
        # Print Position table

        print("\nPositions in the Database To Sell 1 or More Days After the Date Shown:")
        print("\n")
        print("Stock | Quantity | Avg. Price | Purchase Date or The 1st Day This Robot Began Working ")
        print("\n")
        for record in session.query(Position).all():
            print(record.symbol, record.quantity, record.avg_price, record.purchase_date)
        print("\n")


def get_stocks_to_trade():
    try:
        with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
            stock_symbols = [line.strip() for line in file.readlines()]

        if not stock_symbols:  # keep this under the w in with
            print("\n")
            print("************************************************************************************")
            print("Error: The file electricity-or-utility-stocks-to-buy-list.txt doesn't contain any stock symbols.")
            print("This Robot does not work until you place stock symbols in the file named: ")
            print("electricity-or-utility-stocks-to-buy-list.txt ")
            print("************************************************************************************")
            print("\n")

        return stock_symbols  # keep this under the i in if
    except FileNotFoundError:  # keep this under the t in try
        print("\n")
        print("*********************************************************************")
        print("Error: File not found: electricity-or-utility-stocks-to-buy-list.txt ")
        print("*********************************************************************")
        print("\n")
        return []


def remove_symbol_from_trade_list(symbol):
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
        lines = file.readlines()
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'w') as file:
        for line in lines:
            if line.strip() != symbol:
                file.write(line)


def get_opening_price(symbol):
    stock_data = yf.Ticker(symbol)
    # Fetch the stock data for today and get the opening price
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)


def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="5d")["Close"].iloc[-1], 4)


def get_atr_high_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price + 0.40 * atr_value, 4)


def get_atr_low_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price - 0.10 * atr_value, 4)


def get_average_true_range(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='30d')
    atr = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=22)
    return atr[-1]


def status_printer_buy_stocks():
    print(f"\rBuy stocks function is working correctly right now. Checking stocks to buy.....", end='', flush=True)
    # After the loop, print a newline character to move to the next line with the print command below.
    print()   # keep this under the f in for


def status_printer_sell_stocks():
    print(f"\rSell stocks function is working correctly right now. Checking stocks to sell.....", end='', flush=True)
    # After the loop, print a newline character to move to the next line with the print command below.
    print()  # keep this under the f in for


def buy_stocks(bought_stocks, stocks_to_buy, buy_sell_lock):
    stocks_to_remove = []

    for symbol in stocks_to_buy:
        today_date = datetime.today().date()
        current_price = get_current_price(symbol)
        opening_price = get_opening_price(symbol)

        cash_available = round(float(api.get_account().cash), 2)

        qty_of_one_stock = 1

        # Calculate the total cost if we buy 'qty_of_one_stock' shares
        total_cost_for_qty = current_price * qty_of_one_stock

        # - 0.9% is often the top 15% - 17% of electricity stocks 
        # profit buy price setting: 0.9% subtracted from the opening price
        profit_buy_price_setting = opening_price * 0.009

        # Never calculate ATR for a buy price or sell price because it is too slow. 1 second per stock. 
        # Checking that we have enough money for the total_cost_for_qty.
        # Checking if the current price is equal to or less than the atr low price to buy stock.
        # It is also important to check that the current price is less than the opening price by 0.8%
        # before buying the stock. This check is with the profit_buy_price_setting.

        status_printer_buy_stocks()

        if (cash_available >= total_cost_for_qty and current_price <= profit_buy_price_setting):
            api.submit_order(symbol=symbol, qty=qty_of_one_stock, side='buy', type='market', time_in_force='day')
            print(f" {today_date} , Bought {qty_of_one_stock} shares of {symbol} at {current_price}")
            logging.info(f" {today_date} , Bought {qty_of_one_stock} shares of {symbol} at {current_price}")
            stocks_to_remove.append((symbol, current_price, today_date))  # Append tuple

            time.sleep(2)  # keep this under the s in stocks

        time.sleep(2)  # keep this under the i in if. this stops after checking each stock price

    # I might not need the extra sleep command below
    # keep the below time.sleep(1) below the f in for.
    #time.sleep(1)  # wait 1 second to not move too fast for the yfinance rate limit.

    with buy_sell_lock:
        for symbol, price, date in stocks_to_remove:  # Unpack tuple
            bought_stocks[symbol] = (round(price, 4), date)
            stocks_to_buy.remove(symbol)
            remove_symbol_from_trade_list(symbol)
            trade_history = TradeHistory(symbol=symbol, action='buy', quantity=qty_of_one_stock, price=price, date=date)
            session.add(trade_history)
            db_position = Position(symbol=symbol, quantity=qty_of_one_stock, avg_price=price, purchase_date=date)
            session.add(db_position)
        session.commit()  # keep this under the f in for

        refresh_after_buy()  # keep this under the s in session


def refresh_after_buy():
    global stocks_to_buy, bought_stocks
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = update_bought_stocks_from_api()


def update_bought_stocks_from_api():
    positions = api.list_positions()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_entry_price = float(position.avg_entry_price)
        purchase_date = datetime.today()  # Set the date to today
        bought_stocks[symbol] = (avg_entry_price, purchase_date)
        db_position = session.query(Position).filter_by(symbol=symbol).first()
        if db_position:
            db_position.quantity = position.qty
            db_position.avg_price = avg_entry_price
            db_position.purchase_date = purchase_date
        else:
            db_position = Position(symbol=symbol, quantity=position.qty, avg_price=avg_entry_price,
                                   purchase_date=purchase_date)
            session.add(db_position)
    session.commit()  # keep this under the f in for
    return bought_stocks  # keep this under the s in session


def sell_stocks(bought_stocks, buy_sell_lock):
    stocks_to_remove = []

    today_date = datetime.today().date()
    for symbol, (bought_price, bought_date) in bought_stocks.items():

        status_printer_sell_stocks()

        # Convert today_date to datetime
        today_datetime = datetime.combine(today_date, datetime.min.time())
        
        # Check if the stock was purchased at least one day before today
        if bought_date < today_datetime: 
            continue  # Skip this stock if it was purchased today or in the future
        current_price = get_current_price(symbol)
        position = api.get_position(symbol)  # Get the position details from Alpaca API
        bought_price = float(position.avg_entry_price)  # The price you purchased the stock for.

        # Never calculate ATR for a buy price or sell price because it is too slow. 1 second per stock.

        # Sell stocks if the current price is more than 1.6% higher than the purchase price.
        if current_price >= bought_price * 1.016:
            qty = api.get_position(symbol).qty
            api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
            print(f" {today_date}, Sold {qty} shares of {symbol} at {current_price} based on a higher selling price")
            logging.info(
                f" {today_date}, Sold {qty} shares of {symbol} at {current_price} based on a higher selling price")
            stocks_to_remove.append(symbol)  # Append symbols to remove

            time.sleep(2)  # keep this under the s in stocks

        time.sleep(2) # keep this under the i in if. this stops after checking each stock price

    # I might not need the extra sleep command below
    # keep the below time.sleep(1) below the f in for.
    #time.sleep(1)  # wait 1 second to not move too fast for the yfinance rate limit.

    with buy_sell_lock:
        for symbol in stocks_to_remove:
            del bought_stocks[symbol]  # Delete symbols here
            trade_history = TradeHistory(symbol=symbol, action='sell', quantity=qty, price=current_price,
                                         date=today_date)
            session.add(trade_history)
            session.query(Position).filter_by(symbol=symbol).delete()
        session.commit()  # keep this under the f in for

        refresh_after_sell()  # keep this under the s in session


def refresh_after_sell():
    global bought_stocks
    bought_stocks = update_bought_stocks_from_api()


def main():
    global stocks_to_buy
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = load_positions_from_database()
    buy_sell_lock = threading.Lock()

    while True:
        try:
            stop_if_stock_market_is_closed()    # comment this line to debug the Python code
            now = datetime.now(pytz.timezone('US/Eastern'))
            current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")

            cash_balance = round(float(api.get_account().cash), 2)
            print("------------------------------------------------------------------------------------")
            print("2023 Edition of the Advanced Stock Market Trading Robot, Version 2 ")
            print("by https://github.com/CodeProSpecialist")
            print("------------------------------------------------------------------------------------")
            print(f"  {current_time_str} Cash Balance: ${cash_balance}")
            day_trade_count = api.get_account().daytrade_count
            print("\n")
            print(f"Current day trade number: {day_trade_count} out of 3 in 5 business days")
            print("\n")
            print("This Advanced Stock Market Trading Robot is designed to start running ")
            print("after you already own 8 to 28 stock positions. ")
            print("This Robot is programmed to only Sell the stocks that are currently in ")
            print("This Robot's Database. ")
            print("If no Positions are listed below, and you own stock ")
            print("Positions then: 1.) Place 8 to 28 stock symbols to buy in the file named: ")
            print("electricity-or-utility-stocks-to-buy-list.txt, 2.) Stop this program, ")
            print("3.) Delete the trading_bot.db file, and 4.) restart this Robot. ")
            print("\n")
            print("Make sure you see your owned stock Positions listed below ")
            print("in the section named: 'Positions in the Database To Sell 1 or More Days After the Date Shown' ")
            print("for the Robot To Sell the stock positions 1 day after the purchased date shown. ")
            print("\n")
            print("------------------------------------------------------------------------------------")
            print("\n")

            stocks_to_buy = get_stocks_to_trade()

            if not bought_stocks:
                bought_stocks = update_bought_stocks_from_api()

            # the below threads will run the buy_stocks and the sell_stocks functions at the same time
            # in parallel to buy and sell more without taking more time than necessary.

            # keep the below python code below the i in if not bought stocks
            # Create threads for buy_stocks and sell_stocks
            buy_thread = threading.Thread(target=buy_stocks, args=(bought_stocks, stocks_to_buy, buy_sell_lock))
            sell_thread = threading.Thread(target=sell_stocks, args=(bought_stocks, buy_sell_lock))

            # Start both threads
            buy_thread.start()
            sell_thread.start()

            # Wait for both threads to finish
            buy_thread.join()
            sell_thread.join()

            print("\n")
            print("------------------------------------------------------------------------------------")
            print("\n")
            print("Stocks to Purchase:")
            print("\n")
            for symbol in stocks_to_buy:
                current_price = get_current_price(symbol)

                print(f"Symbol: {symbol} | Current Price: {current_price} ")
                time.sleep(1)  # wait 1 second to not move too fast for the yfinance rate limit.
            print("\n")
            print("------------------------------------------------------------------------------------")
            print("\n")

            print_database_tables()

            # account = api.get_account()
            # print(account)   # uncomment to print Alpaca Account details to debug the software

            if DEBUG:
                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
                print("Stocks to Purchase:")
                print("\n")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    atr_low_price = get_atr_low_price(symbol)
                    print(
                        f"Symbol: {symbol} | Current Price: {current_price} | ATR low buy signal price: {atr_low_price}")

                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
                print("\nStocks to Sell:")
                print("\n")
                for symbol, _ in bought_stocks.items():
                    current_price = get_current_price(symbol)
                    atr_high_price = get_atr_high_price(symbol)
                    print(
                        f"Symbol: {symbol} | Current Price: {current_price} | ATR high sell signal profit price: {atr_high_price}")

                print("\n")

            # keep the below time.sleep(60) to 60 seconds because yfinance api 
            # will stop the stock data feed for the reason of exceeding the rate limit or from this program being too fast. 
            print("Waiting 60 seconds before checking price data again........")
            time.sleep(60)  # keep this under the i in if

        except Exception as e:
            logging.error(f"Error encountered: {e}")
            time.sleep(120)  # keep this under the l in logging


def load_positions_from_database():
    positions = session.query(Position).all()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_price = position.avg_price
        purchase_date = position.purchase_date
        bought_stocks[symbol] = (avg_price, purchase_date)
    return bought_stocks


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Error encountered: {e}")
        session.close()
