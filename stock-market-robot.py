import threading
import logging
import csv
import os
import time
import schedule
from datetime import datetime, timedelta, time as time2
import pytz
import alpaca_trade_api as tradeapi
import yfinance as yf
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# Global variables
stocks_to_buy = []
today_date = None
today_datetime = None
csv_writer = None
csv_filename = 'log-file-of-buy-and-sell-signals.csv'
fieldnames = ['Date', 'Buy', 'Sell', 'Quantity', 'Symbol', 'Price Per Share']
price_changes = {}
end_time = 0

# Configuration flags
PRINT_STOCKS_TO_BUY = False  # Keep False for faster execution
PRINT_ROBOT_STORED_BUY_AND_SELL_LIST_DATABASE = True  # Keep False for faster execution
PRINT_DATABASE = True  # Keep True to view stocks to sell
DEBUG = False  # Keep False for faster execution
POSITION_DATES_AS_YESTERDAY_OPTION = False  # Keep False to not change dates of owned stocks

# Set timezone to Eastern
eastern = pytz.timezone('US/Eastern')

# Dictionaries for tracking prices
stock_data = {}
previous_prices = {}
buy_sell_lock = threading.Lock()

# Logging setup
logging.basicConfig(filename='trading-bot-program-logging-messages.txt', level=logging.INFO)

# CSV setup
with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Database Models
Base = sqlalchemy.orm.declarative_base()

class TradeHistory(Base):
    __tablename__ = 'trade_history'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    action = Column(String)
    quantity = Column(Float)  # Changed from Integer to Float to support fractional shares
    price = Column(Float)
    date = Column(String)

class Position(Base):
    __tablename__ = 'positions'
    symbol = Column(String, primary_key=True)
    quantity = Column(Float)  # Changed from Integer to Float to support fractional shares
    avg_price = Column(Float)
    purchase_date = Column(String)

# Initialize SQLAlchemy
engine = create_engine('sqlite:///trading_bot.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def stop_if_stock_market_is_closed():
    market_open_time = time2(9, 27)
    market_close_time = time2(16, 0)
    while True:
        now = datetime.now(eastern)
        current_time = now.time()
        if now.weekday() <= 4 and market_open_time <= current_time <= market_close_time:
            break
        print("\n")
        print('''
            2024 Edition of the Bull Market Advanced Stock Market Trading Robot, Version 5 
           _____   __                   __             ____            __            __ 
          / ___/  / /_  ____   _____   / /__          / __ \  ____    / /_   ____   / /_
          \__ \  / __/ / __ \ / ___/  / //_/         / /_/ / /    \  / __ \ / __/
         ___/ / / /_  / /_/ // /__   / ,<           / _, _/ / /_/ / / /_/ // /_/ // /_  
        /____/  \__/  \____/ \___/  /_/|_|         /_/ |_|  \____/ /_.___/ \____/ \__/  
                                                  https://github.com/CodeProSpecialist
                       Featuring an Accelerated Database Engine with Python 3 SQLAlchemy  
         ''')
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %I:%M:%S %p")}')
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Stockbot begins watching stock prices early at 9:27 am Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        print("\n")
        time.sleep(60)

def print_database_tables():
    if PRINT_DATABASE:
        positions = api.list_positions()
        show_price_percentage_change = True
        print("\nTrade History In This Robot's Database:")
        print("\nStock | Buy or Sell | Quantity | Avg. Price | Date \n")
        for record in session.query(TradeHistory).all():
            print(f"{record.symbol} | {record.action} | {record.quantity:.4f} | {record.price:.2f} | {record.date}")
        print("-------------------------------------------------------")
        print("\nPositions in the Database To Sell 1 or More Days After the Date Shown:")
        print("\nStock | Quantity | Avg. Price | Date or The 1st Day This Robot Began Working \n")
        for record in session.query(Position).all():
            symbol, quantity, avg_price, purchase_date = record.symbol, record.quantity, record.avg_price, record.purchase_date
            if show_price_percentage_change:
                current_price = get_current_price(symbol)
                percentage_change = ((current_price - avg_price) / avg_price) * 100
                print(f"{record.symbol} | {record.quantity:.4f} | {record.avg_price:.2f} | {record.purchase_date} | Price Change: {percentage_change:.2f}%")
            else:
                print(f"{record.symbol} | {record.quantity:.4f} | {record.avg_price:.2f} | {record.purchase_date}")
        print("\n")

def get_stocks_to_trade():
    try:
        with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
            stock_symbols = [line.strip() for line in file.readlines()]
        if not stock_symbols:
            print("\n**********************************************************************")
            print("*   Error: The file electricity-or-utility-stocks-to-buy-list.txt doesn't contain any stock symbols.   *")
            print("*   This Robot does not work until you place stock symbols in the file named:                  *")
            print("*       electricity-or-utility-stocks-to-buy-list.txt                                          *")
            print("**********************************************************************\n")
        return stock_symbols
    except FileNotFoundError:
        print("\n********************************************")
        print("*   Error: File not found: electricity-or-utility-stocks-to-buy-list.txt   *")
        print("********************************************\n")
        return []

def remove_symbol_from_trade_list(symbol):
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'r') as file:
        lines = file.readlines()
    with open('electricity-or-utility-stocks-to-buy-list.txt', 'w') as file:
        for line in lines:
            if line.strip() != symbol:
                file.write(line)

def get_opening_price(symbol):
    symbol = symbol.replace('.', '-')  # Replace '.' with '-' for yfinance
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)

def get_current_price(symbol):
    symbol = symbol.replace('.', '-')  # Replace '.' with '-' for yfinance
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period='1d')['Close'].iloc[0], 4)

def get_atr_high_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price + 0.40 * atr_value, 4)

def get_atr_low_price(symbol):
    atr_value = get_average_true_range(symbol)
    current_price = get_current_price(symbol)
    return round(current_price - 0.10 * atr_value, 4)

def get_average_true_range(symbol):
    symbol = symbol.replace('.', '-')  # Replace '.' with '-' for yfinance
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='30d')
    high = data['High']
    low = data['Low']
    close = data['Close']
    atr = AverageTrueRange(high, low, close, window=22)
    return atr.average_true_range().iloc[-1]

def status_printer_buy_stocks():
    print(f"\rBuy stocks function is working correctly right now. Checking stocks to buy.....", end='', flush=True)
    print()

def status_printer_sell_stocks():
    print(f"\rSell stocks function is working correctly right now. Checking stocks to sell.....", end='', flush=True)
    print()

def calculate_technical_indicators(symbol, lookback_days=90):
    symbol = symbol.replace('.', '-')  # Replace '.' with '-' for yfinance compatibility
    stock_data = yf.Ticker(symbol)
    historical_data = stock_data.history(period=f'{lookback_days}d')
    close = historical_data['Close']
    high = historical_data['High']
    low = historical_data['Low']
    volume = historical_data['Volume']

    # Calculate MACD using ta library
    short_window = 12
    long_window = 26
    signal_window = 9
    macd_indicator = MACD(close, window_fast=short_window, window_slow=long_window, window_sign=signal_window)
    historical_data['macd'] = macd_indicator.macd()
    historical_data['signal'] = macd_indicator.macd_signal()

    # Calculate RSI using ta library
    rsi_period = 14
    historical_data['rsi'] = RSIIndicator(close, window=rsi_period).rsi()

    # Volume
    historical_data['volume'] = volume

    return historical_data

def print_technical_indicators(symbol, historical_data):
    print(f"\nTechnical Indicators for {symbol}:\n")
    print(historical_data[['Close', 'macd', 'signal', 'rsi', 'volume']].tail())
    print("")

def calculate_cash_on_hand():
    cash_available = round(float(api.get_account().cash), 2)
    return cash_available

def calculate_total_symbols(stocks_to_buy):
    return len(stocks_to_buy)

def allocate_cash_equally(cash_available, total_symbols):
    max_allocation_per_symbol = 600
    allocation_per_symbol = min(max_allocation_per_symbol, cash_available) / total_symbols if total_symbols > 0 else 0
    return allocation_per_symbol

def get_previous_price(symbol):
    if symbol in previous_prices:
        return previous_prices[symbol]
    else:
        current_price = get_current_price(symbol)
        previous_prices[symbol] = current_price
        print(f"No previous price for {symbol} was found. Using the current price as the previous price: {current_price}")
        return current_price

def update_previous_price(symbol, current_price):
    previous_prices[symbol] = current_price

def run_schedule():
    while not end_time_reached():
        schedule.run_pending()
        time.sleep(1)

def track_price_changes(symbol):
    current_price = get_current_price(symbol)
    previous_price = get_previous_price(symbol)
    print("")
    print_technical_indicators(symbol, calculate_technical_indicators(symbol))
    print("")
    if current_price > previous_price:
        price_changes[symbol]['increased'] += 1
        print(f"{symbol} price just increased | current price: {current_price}")
        time.sleep(5)
    elif current_price < previous_price:
        price_changes[symbol]['decreased'] += 1
        print(f"{symbol} price just decreased | current price: {current_price}")
        time.sleep(5)
    else:
        print(f"{symbol} price has not changed | current price: {current_price}")
        time.sleep(5)
    time.sleep(1)
    update_previous_price(symbol, current_price)
    return 'increase' if current_price > previous_price else 'decrease' if current_price < previous_price else 'no_change'

def end_time_reached():
    return time.time() >= end_time

def buy_stocks(bought_stocks, stocks_to_buy, buy_sell_lock):
    stocks_to_remove = []
    global start_time, end_time, original_start_time, price_changes, buy_stock_green_light

    buy_stock_green_light = 0
    extracted_date_from_today_date = datetime.today().date()
    today_date_str = extracted_date_from_today_date.strftime("%Y-%m-%d")
    now = datetime.now(pytz.timezone('US/Eastern'))
    current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")
    start_trading_time = datetime.now(pytz.timezone('US/Eastern')).replace(hour=10, minute=2, second=0, microsecond=0)

    if datetime.now(pytz.timezone('US/Eastern')) < start_trading_time:
        return

    start_time = time.time()
    original_start_time = start_time
    end_time = start_time + 3 * 60
    target_time = datetime.now(pytz.timezone('US/Eastern')).replace(hour=15, minute=56, second=0, microsecond=0)

    if datetime.now(pytz.timezone('US/Eastern')) > target_time:
        print("\nReturning and Exiting from the Buy Stocks function because we are outside of the buy strategy times.\n")
        return
    else:
        print("\nContinuing with the Buy Stocks function.\n")

    price_changes = {symbol: {'increased': 0, 'decreased': 0} for symbol in stocks_to_buy}

    try:
        while not end_time_reached():
            for symbol in stocks_to_buy:
                cash_available = calculate_cash_on_hand()
                total_symbols = calculate_total_symbols(stocks_to_buy)
                allocation_per_symbol = allocate_cash_equally(cash_available, total_symbols)
                current_price = get_current_price(symbol)
                qty_of_one_stock = int(allocation_per_symbol / current_price) if current_price > 0 else 0

                if not hasattr(buy_stocks, 'scheduled_task'):
                    buy_stocks.scheduled_task = schedule.every(5).seconds.do(track_price_changes, symbol)
                    schedule_thread = threading.Thread(target=run_schedule)
                    schedule_thread.start()

                change_type = track_price_changes(symbol)
                if change_type == 'increase':
                    price_changes[symbol]['increased'] += 1
                elif change_type == 'decrease':
                    price_changes[symbol]['decreased'] += 1

                print(f"\nTotal Price Increases for {symbol}: {price_changes[symbol]['increased']}")
                print(f"Total Price Decreases for {symbol}: {price_changes[symbol]['decreased']}\n")
                time.sleep(5)

        if end_time_reached():
            for symbol in stocks_to_buy:
                cash_available = calculate_cash_on_hand()
                total_symbols = calculate_total_symbols(stocks_to_buy)
                allocation_per_symbol = allocate_cash_equally(cash_available, total_symbols)
                current_price = get_current_price(symbol)
                qty_of_one_stock = int(allocation_per_symbol / current_price) if current_price > 0 else 0
                total_cost_for_qty = current_price * qty_of_one_stock

                print("\n")
                status_printer_buy_stocks()
                print(f"\nSymbol: {symbol}")
                print(f"Current Price: {current_price}")
                print(f"Qty of One Stock: {qty_of_one_stock}")
                print(f"Total Cost for Qty: {total_cost_for_qty}")
                print(f"Cash Available: {cash_available}")
                print(f"Increased: {price_changes[symbol]['increased']}")
                print(f"Decreased: {price_changes[symbol]['decreased']}")
                print(f"End Time Reached for waiting 30 seconds: {end_time_reached()}\n")

                total_increases = price_changes[symbol]['increased']
                total_decreases = price_changes[symbol]['decreased']
                print(f"Total Price Increases for {symbol}: {total_increases}")
                print(f"Total Price Decreases for {symbol}: {total_decreases}\n")

                overall_total_increases = sum(price_changes[symbol]['increased'] for symbol in stocks_to_buy)
                overall_total_decreases = sum(price_changes[symbol]['decreased'] for symbol in stocks_to_buy)
                print(f"Overall Total Price Increases: {overall_total_increases}")
                print(f"Overall Total Price Decreases: {overall_total_decreases}\n")

                historical_data = calculate_technical_indicators(symbol, lookback_days=90)
                macd_value = historical_data['macd'].iloc[-1]
                rsi_value = historical_data['rsi'].iloc[-1]
                volume_value = historical_data['volume'].iloc[-1]

                print(f"MACD: {macd_value}")
                print(f"RSI: {rsi_value}")
                print(f"Volume: {volume_value}\n")

                favorable_macd_condition = historical_data['signal'].iloc[-1] > 0.15
                favorable_rsi_condition = historical_data['rsi'].iloc[-1] > 70
                favorable_volume_condition = historical_data['volume'].iloc[-1] > 0.85 * historical_data['volume'].mean()

                if (cash_available >= total_cost_for_qty and
                        price_changes[symbol]['increased'] >= 3 and
                        price_changes[symbol]['increased'] > price_changes[symbol]['decreased'] and
                        favorable_macd_condition and favorable_rsi_condition and favorable_volume_condition):
                    if qty_of_one_stock > 0:
                        print(f"\n ******** Buying stocks for {symbol} with limit order... *************************************** \n")
                        print_technical_indicators(symbol, calculate_technical_indicators(symbol))
                        symbol_for_order = symbol.replace('-', '.')  # Adjust symbol for Alpaca API
                        try:
                            # Place limit order at current price
                            limit_order = api.submit_order(
                                symbol=symbol_for_order,
                                qty=qty_of_one_stock,
                                side='buy',
                                type='limit',
                                limit_price=current_price,
                                time_in_force='day'
                            )
                            print(f"\n {current_time_str} , Placed limit buy order for {qty_of_one_stock} shares of {symbol_for_order} at {current_price}\n")
                            
                            # Wait 1 minute and 30 seconds
                            print(f"\nWaiting 1 minute and 30 seconds to confirm if {symbol_for_order} is in owned positions...\n")
                            time.sleep(90)

                            # Check if symbol is in owned positions
                            positions = api.list_positions()
                            symbol_owned = any(pos.symbol == symbol_for_order for pos in positions)
                            
                            if not symbol_owned:
                                print(f"\n{symbol_for_order} not found in owned positions. Placing market order...\n")
                                try:
                                    # Place market order
                                    market_order = api.submit_order(
                                        symbol=symbol_for_order,
                                        qty=qty_of_one_stock,
                                        side='buy',
                                        type='market',
                                        time_in_force='day'
                                    )
                                    print(f"\n {current_time_str} , Placed market buy order for {qty_of_one_stock} shares of {symbol_for_order} at market price\n")
                                except Exception as e:
                                    print(f"Error placing market buy order for {symbol_for_order}: {str(e)}")
                                    logging.error(f"Error placing market buy order for {symbol_for_order}: {str(e)}")
                                    continue  # Skip to next symbol if market order fails
                            else:
                                print(f"\n{symbol_for_order} found in owned positions after limit order.\n")

                            # Log the buy order (limit or market) to CSV
                            with open(csv_filename, mode='a', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                csv_writer.writerow(
                                    {'Date': current_time_str, 'Buy': 'Buy', 'Quantity': qty_of_one_stock, 'Symbol': symbol_for_order,
                                     'Price Per Share': current_price})
                            stocks_to_remove.append((symbol, current_price, today_date_str))
                            buy_stock_green_light = 1

                            # Wait 1 minute and 30 seconds before placing trailing stop sell order
                            print(f"\nWaiting 1 minute and 30 seconds before checking for open sell orders and placing trailing stop sell order for {symbol_for_order}...\n")
                            time.sleep(90)

                            # Check for open sell orders before placing trailing stop
                            open_sell_orders = api.list_orders(status='open', side='sell', symbol=symbol_for_order)
                            if not open_sell_orders:
                                stop_order_id = place_trailing_stop_sell_order(symbol_for_order, qty_of_one_stock, current_price)
                                if stop_order_id:
                                    print(f"Trailing stop sell order placed for {symbol_for_order} with ID: {stop_order_id}\n")
                                else:
                                    print(f"Failed to place trailing stop sell order for {symbol_for_order}\n")
                            else:
                                print(f"Open sell order(s) exist for {symbol_for_order}. Skipping trailing stop sell order.\n")
                        except Exception as e:
                            print(f"Error placing limit buy order for {symbol_for_order}: {str(e)}")
                            logging.error(f"Error placing limit buy order for {symbol_for_order}: {str(e)}")
                            buy_stock_green_light = 0
                    else:
                        # Insufficient cash to buy one share, use market order with 20% of available cash
                        notional_amount = min(0.2 * cash_available, allocation_per_symbol)
                        if notional_amount >= 0.01:  # Alpaca requires minimum $0.01 for notional orders
                            print(f"\n ******** Insufficient cash to buy one share of {symbol}. Buying with market order using ${notional_amount:.2f} (up to 20% of available cash)... *************************************** \n")
                            print_technical_indicators(symbol, calculate_technical_indicators(symbol))
                            symbol_for_order = symbol.replace('-', '.')  # Adjust symbol for Alpaca API
                            try:
                                # Place market order with notional amount
                                market_order = api.submit_order(
                                    symbol=symbol_for_order,
                                    notional=notional_amount,
                                    side='buy',
                                    type='market',
                                    time_in_force='day'
                                )
                                # Get the actual quantity filled from the order
                                order = api.get_order(market_order.id)
                                qty_filled = float(order.filled_qty) if order.filled_qty else 0
                                print(f"\n {current_time_str} , Placed market buy order for {qty_filled:.4f} shares of {symbol_for_order} using ${notional_amount:.2f}\n")
                                
                                # Log the buy order to CSV
                                with open(csv_filename, mode='a', newline='') as csv_file:
                                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                    csv_writer.writerow(
                                        {'Date': current_time_str, 'Buy': 'Buy', 'Quantity': qty_filled, 'Symbol': symbol_for_order,
                                         'Price Per Share': current_price})
                                stocks_to_remove.append((symbol, current_price, today_date_str))
                                buy_stock_green_light = 1

                                # Wait 1 minute and 30 seconds before placing trailing stop sell order
                                print(f"\nWaiting 1 minute and 30 seconds before checking for open sell orders and placing trailing stop sell order for {symbol_for_order}...\n")
                                time.sleep(90)

                                # Check for open sell orders before placing trailing stop
                                open_sell_orders = api.list_orders(status='open', side='sell', symbol=symbol_for_order)
                                if not open_sell_orders and qty_filled > 0:
                                    stop_order_id = place_trailing_stop_sell_order(symbol_for_order, qty_filled, current_price)
                                    if stop_order_id:
                                        print(f"Trailing stop sell order placed for {symbol_for_order} with ID: {stop_order_id}\n")
                                    else:
                                        print(f"Failed to place trailing stop sell order for {symbol_for_order}\n")
                                else:
                                    print(f"Open sell order(s) exist for {symbol_for_order} or no shares filled. Skipping trailing stop sell order.\n")
                            except Exception as e:
                                print(f"Error placing market buy order for {symbol_for_order}: {str(e)}")
                                logging.error(f"Error placing market buy order for {symbol_for_order}: {str(e)}")
                                buy_stock_green_light = 0
                        else:
                            print(f"\nInsufficient cash to buy {symbol} even with 20% of available cash (${notional_amount:.2f}). Skipping.\n")
                            buy_stock_green_light = 0
                else:
                    print("\nNot buying stocks based on the technical indicators: MACD, RSI, VOLUME, or based on price decreases.\n")
                    print_technical_indicators(symbol, calculate_technical_indicators(symbol))
                    print("")
                time.sleep(2)
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred in buy_stocks: {str(e)}")
        logging.error(f"Error in buy_stocks: {str(e)}")
        start_time = original_start_time
        end_time = start_time + 102 * 60
        schedule_thread = threading.Thread(target=run_schedule)
        schedule_thread.start()

    try:
        with buy_sell_lock:
            for symbol, price, date in stocks_to_remove:
                symbol_for_db = symbol.replace('-', '.')  # Ensure consistent symbol format
                bought_stocks[symbol_for_db] = (round(price, 4), date)
                stocks_to_buy.remove(symbol)
                remove_symbol_from_trade_list(symbol)
                trade_history = TradeHistory(symbol=symbol_for_db, action='buy', quantity=qty_of_one_stock if qty_of_one_stock > 0 else qty_filled, price=price, date=date)
                session.add(trade_history)
                db_position = Position(symbol=symbol_for_db, quantity=qty_of_one_stock if qty_of_one_stock > 0 else qty_filled, avg_price=price, purchase_date=date)
                session.add(db_position)
            session.commit()
            refresh_after_buy()
            account_info = api.get_account()
            day_trade_count = account_info.daytrade_count
            if buy_stock_green_light == 1 and day_trade_count < 3:
                print(f"\nDay trade count: {day_trade_count} out of 3 in 5 business days\n")
            else:
                print(f"\nDay trade limit reached or no buy executed. Day trade count: {day_trade_count}\n")
    except SQLAlchemyError as e:
        print(f"Database error in buy_stocks: {str(e)}")
        logging.error(f"Database error in buy_stocks: {str(e)}")
        session.rollback()

def refresh_after_buy():
    global stocks_to_buy, bought_stocks
    time.sleep(2)
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = update_bought_stocks_from_api()

def place_trailing_stop_sell_order(symbol, qty_of_one_stock, current_price):
    try:
        # Check for open sell orders
        open_sell_orders = api.list_orders(status='open', side='sell', symbol=symbol)
        if open_sell_orders:
            print(f"Cannot place trailing stop sell order for {symbol}: Existing open sell order(s) found.")
            logging.info(f"Cannot place trailing stop sell order for {symbol}: Existing open sell order(s) found.")
            return None

        stop_loss_percent = 1.0
        stop_loss_price = current_price * (1 - stop_loss_percent / 100)
        symbol = symbol.replace('-', '.')  # Ensure correct symbol format
        stop_order = api.submit_order(
            symbol=symbol,
            qty=qty_of_one_stock,
            side='sell',
            type='trailing_stop',
            trail_percent=stop_loss_percent,
            time_in_force='gtc'
        )
        print(f"Placed trailing stop sell order for {qty_of_one_stock:.4f} shares of {symbol} at {stop_loss_price:.2f}")
        logging.info(f"Placed trailing stop sell order for {qty_of_one_stock:.4f} shares of {symbol} at {stop_loss_price:.2f}")
        with buy_sell_lock:
            if symbol in bought_stocks:
                del bought_stocks[symbol]
                db_position = session.query(Position).filter_by(symbol=symbol).first()
                if db_position:
                    session.delete(db_position)
                    session.commit()
        return stop_order.id
    except Exception as e:
        print(f"Error placing trailing stop sell order for {symbol}: {str(e)}")
        logging.error(f"Error placing trailing stop sell order for {symbol}: {str(e)}")
        return None

def update_bought_stocks_from_api():
    positions = api.list_positions()
    bought_stocks = {}
    yesterday = datetime.today() - timedelta(days=1)
    run_counter_file = "trading_bot_run_counter.txt"
    if not os.path.exists(run_counter_file):
        with open(run_counter_file, "w") as f:
            f.write("0")
        run_counter = 0
    else:
        with open(run_counter_file, "r") as f:
            run_counter = int(f.read())
        run_counter += 1
    for position in positions:
        symbol = position.symbol
        avg_entry_price = float(position.avg_entry_price)
        quantity = float(position.qty)  # Convert to float to handle fractional shares
        try:
            db_position = session.query(Position).filter_by(symbol=symbol).one()
            db_position.quantity = quantity
            db_position.avg_price = avg_entry_price
            if POSITION_DATES_AS_YESTERDAY_OPTION and run_counter < 1:
                db_position.purchase_date = yesterday.strftime("%Y-%m-%d")
        except NoResultFound:
            purchase_date = yesterday if POSITION_DATES_AS_YESTERDAY_OPTION and run_counter < 1 else datetime.today()
            purchase_date_str = purchase_date.strftime("%Y-%m-%d")
            db_position = Position(symbol=symbol, quantity=quantity, avg_price=avg_entry_price, purchase_date=purchase_date_str)
            session.add(db_position)
        bought_stocks[symbol] = (avg_entry_price, db_position.purchase_date)
    with open(run_counter_file, "w") as f:
        f.write(str(run_counter))
    session.commit()
    return bought_stocks

def sell_stocks(bought_stocks, buy_sell_lock):
    stocks_to_remove = []
    now = datetime.now(pytz.timezone('US/Eastern'))
    current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")
    extracted_date_from_today_date = datetime.today().date()
    for symbol, (bought_price, purchase_date) in bought_stocks.items():
        status_printer_sell_stocks()
        today_date_str = extracted_date_from_today_date.strftime("%Y-%m-%d")
        bought_date_str = purchase_date
        if bought_date_str < today_date_str:
            current_price = get_current_price(symbol)
            try:
                position = api.get_position(symbol)
                bought_price = float(position.avg_entry_price)
                open_orders = api.list_orders(status='open', symbol=symbol)
                if open_orders:
                    print(f"There is an open sell order for {symbol}. Skipping sell order.")
                    continue
                if current_price >= bought_price * 1.001:
                    qty = float(position.qty)  # Use float to handle fractional shares
                    api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='day')
                    print(f" {current_time_str}, Sold {qty:.4f} shares of {symbol} at {current_price:.2f} based on a higher selling price.")
                    with open(csv_filename, mode='a', newline='') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        csv_writer.writerow(
                            {'Date': current_time_str, 'Sell': 'Sell', 'Quantity': qty, 'Symbol': symbol, 'Price Per Share': current_price})
                    stocks_to_remove.append(symbol)
                    time.sleep(2)
                time.sleep(2)
            except Exception as e:
                print(f"Error accessing position for {symbol}: {str(e)}")
                logging.error(f"Error accessing position for {symbol}: {str(e)}")
    try:
        with buy_sell_lock:
            for symbol in stocks_to_remove:
                del bought_stocks[symbol]
                trade_history = TradeHistory(symbol=symbol, action='sell', quantity=qty, price=current_price, date=today_date_str)
                session.add(trade_history)
                session.query(Position).filter_by(symbol=symbol).delete()
            session.commit()
            refresh_after_sell()
    except SQLAlchemyError as e:
        print(f"Database error in sell_stocks: {str(e)}")
        logging.error(f"Database error in sell_stocks: {str(e)}")
        session.rollback()

def refresh_after_sell():
    global bought_stocks
    time.sleep(2)
    bought_stocks = update_bought_stocks_from_api()

def load_positions_from_database():
    positions = session.query(Position).all()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_price = position.avg_price
        purchase_date = position.purchase_date
        bought_stocks[symbol] = (avg_price, purchase_date)
    return bought_stocks

def main():
    global stocks_to_buy
    stocks_to_buy = get_stocks_to_trade()
    bought_stocks = load_positions_from_database()
    buy_sell_lock = threading.Lock()
    while True:
        try:
            stop_if_stock_market_is_closed()
            now = datetime.now(pytz.timezone('US/Eastern'))
            current_time_str = now.strftime("Eastern Time | %I:%M:%S %p | %m-%d-%Y |")
            cash_balance = round(float(api.get_account().cash), 2)
            print("-------------------------------------------------------")
            print("2024 Edition of the Bull Market Advanced Stock Market Trading Robot, Version 5 ")
            print("by https://github.com/CodeProSpecialist")
            print("-------------------------------------------------------")
            print(f"  {current_time_str} Cash Balance: ${cash_balance}")
            day_trade_count = api.get_account().daytrade_count
            print(f"\nCurrent day trade number: {day_trade_count} out of 3 in 5 business days\n")
            print("-------------------------------------------------------\n")
            stocks_to_buy = get_stocks_to_trade()
            if not bought_stocks:
                bought_stocks = update_bought_stocks_from_api()
            sell_thread = threading.Thread(target=sell_stocks, args=(bought_stocks, buy_sell_lock))
            buy_thread = threading.Thread(target=buy_stocks, args=(bought_stocks, stocks_to_buy, buy_sell_lock))
            sell_thread.start()
            buy_thread.start()
            sell_thread.join()
            buy_thread.join()
            if PRINT_STOCKS_TO_BUY:
                print("\n-------------------------------------------------------\n")
                print("Stocks to Purchase:\n")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} ")
                    time.sleep(1)
                print("\n-------------------------------------------------------\n")
            if PRINT_ROBOT_STORED_BUY_AND_SELL_LIST_DATABASE:
                print_database_tables()
            if DEBUG:
                print("\n-------------------------------------------------------\n")
                print("Stocks to Purchase:\n")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    atr_low_price = get_atr_low_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} | ATR low buy signal price: {atr_low_price}")
                print("\n-------------------------------------------------------\n")
                print("\nStocks to Sell:\n")
                for symbol, _ in bought_stocks.items():
                    current_price = get_current_price(symbol)
                    atr_high_price = get_atr_high_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} | ATR high sell signal profit price: {atr_high_price}")
                print("\n")
            print("Do Not Stop this Robot or you will need to ")
            print("delete the trading_bot.db database file and start over again with an empty database. ")
            print("Placing trades without this Robot will also require ")
            print("deleting the trading_bot.db database file and starting over again with an empty database. ")
            print("\nWaiting 60 seconds before checking price data again........\n")
            time.sleep(60)
        except Exception as e:
            print(f"Error in main: {str(e)}")
            logging.error(f"Error in main: {str(e)}")
            time.sleep(120)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in main: {str(e)}")
        logging.error(f"Error in main: {str(e)}")
        session.close()
