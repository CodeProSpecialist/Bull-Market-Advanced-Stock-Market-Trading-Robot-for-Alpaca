import threading
import logging
import csv
import os
import time
from datetime import datetime, timedelta, date
from datetime import time as time2
import alpaca_trade_api as tradeapi
import pytz
import talib
import yfinance as yf
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

global stocks_to_buy, today_date, today_datetime, csv_writer, csv_filename, fieldnames, price_changes, end_time

# Configuration flags
PRINT_STOCKS_TO_BUY = False
PRINT_ROBOT_STORED_BUY_AND_SELL_LIST_DATABASE = True
PRINT_DATABASE = True
DEBUG = False
POSITION_DATES_AS_YESTERDAY_OPTION = False

# Set timezone to Eastern
eastern = pytz.timezone('US/Eastern')

# Dictionaries for price tracking
stock_data = {}
previous_prices = {}
end_time = 0
api_time_format = '%Y-%m-%dT%H:%M:%S.%f-04:00'
buy_sell_lock = threading.Lock()

# Logging setup
logging.basicConfig(filename='trading-bot-program-logging-messages.txt', level=logging.INFO)

# CSV setup
csv_filename = 'log-file-of-buy-and-sell-signals.csv'
fieldnames = ['Date', 'Buy', 'Sell', 'Quantity', 'Symbol', 'Price Per Share']

with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Define the Database Models
Base = sqlalchemy.orm.declarative_base()

class TradeHistory(Base):
    __tablename__ = 'trade_history'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    action = Column(String)
    quantity = Column(Float)  # MODIFIED: Changed to Float for fractional shares
    price = Column(Float)
    date = Column(String)

class Position(Base):
    __tablename__ = 'positions'
    symbol = Column(String, primary_key=True)
    quantity = Column(Float)  # MODIFIED: Changed to Float for fractional shares
    avg_price = Column(Float)
    purchase_date = Column(String)

# Initialize SQLAlchemy
engine = create_engine('sqlite:///trading_bot.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# [Other unchanged functions: stop_if_stock_market_is_closed, print_database_tables, get_stocks_to_trade, 
# remove_symbol_from_trade_list, get_opening_price, get_current_price, get_atr_high_price, get_atr_low_price, 
# get_average_true_range, status_printer_buy_stocks, status_printer_sell_stocks, calculate_technical_indicators, 
# print_technical_indicators, calculate_cash_on_hand, calculate_total_symbols, allocate_cash_equally, 
# get_previous_price, update_previous_price, track_price_changes, end_time_reached]

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
        print("")
        print("Exiting buy_stocks: Market trading time not yet reached.")
        return
    target_time = datetime.now(pytz.timezone('US/Eastern')).replace(hour=15, minute=56, second=0, microsecond=0)
    if datetime.now(pytz.timezone('US/Eastern')) > target_time:
        print("")
        print("Exiting buy_stocks: Outside of buy strategy times.")
        print("")
        return
    print("")
    print(f"Starting buy_stocks: Monitoring {len(stocks_to_buy)} symbols simultaneously for 3 minutes each.")
    print("")
    start_time = time.time()
    original_start_time = start_time
    with buy_sell_lock:
        price_changes = {symbol: {'increased': 0, 'decreased': 0} for symbol in stocks_to_buy}
    try:
        threads = []
        for symbol in stocks_to_buy:
            thread = threading.Thread(target=track_price_changes, args=(symbol, 180))
            threads.append(thread)
            print(f"Starting monitoring thread for {symbol}...")
            thread.start()
            time.sleep(10)
        for thread in threads:
            thread.join()
        print("")
        print(f"Completed simultaneous monitoring of all {len(stocks_to_buy)} symbols for 3 minutes each.")
        print("")
        for symbol in stocks_to_buy:
            cash_available = calculate_cash_on_hand()
            total_symbols = calculate_total_symbols(stocks_to_buy)
            allocation_per_symbol = allocate_cash_equally(cash_available, total_symbols)
            current_price = get_current_price(symbol)
            qty_of_one_stock = allocation_per_symbol / current_price  # MODIFIED: Use float for fractional shares
            total_cost_for_qty = current_price * qty_of_one_stock
            print("")
            status_printer_buy_stocks()
            print("")
            print(f"Symbol: {symbol}")
            print(f"Current Price: {current_price}")
            print(f"Qty of One Stock: {qty_of_one_stock:.4f}")
            print(f"Total Cost for Qty: {total_cost_for_qty:.2f}")
            print("")
            print(f"Cash Available: {cash_available}")
            print("")
            print(f"Increased: {price_changes[symbol]['increased']}")
            print(f"Decreased: {price_changes[symbol]['decreased']}")
            print("")
            total_increases = price_changes[symbol]['increased']
            total_decreases = price_changes[symbol]['decreased']
            print("")
            print(f"Total Price Increases for {symbol}: {total_increases}")
            print(f"Total Price Decreases for {symbol}: {total_decreases}")
            print("")
            overall_total_increases = sum(price_changes[symbol]['increased'] for symbol in stocks_to_buy)
            overall_total_decreases = sum(price_changes[symbol]['decreased'] for symbol in stocks_to_buy)
            print("")
            print(f"Overall Total Price Increases: {overall_total_increases}")
            print(f"Overall Total Price Decreases: {overall_total_decreases}")
            print("")
            historical_data = calculate_technical_indicators(symbol, lookback_days=90)
            macd_value = historical_data['macd'].iloc[-1]
            rsi_value = historical_data['rsi'].iloc[-1]
            volume_value = historical_data['volume'].iloc[-1]
            print(f"MACD: {macd_value}")
            print(f"RSI: {rsi_value}")
            print(f"Volume: {volume_value}")
            print("")
            favorable_macd_condition = historical_data['signal'].iloc[-1] > 0.15
            favorable_rsi_condition = historical_data['rsi'].iloc[-1] > 70
            favorable_volume_condition = historical_data['volume'].iloc[-1] > 0.85 * historical_data['volume'].mean()
            if (cash_available >= total_cost_for_qty and
                    price_changes[symbol]['increased'] >= 3 and
                    price_changes[symbol]['increased'] > price_changes[symbol]['decreased'] and
                    favorable_macd_condition and favorable_rsi_condition and favorable_volume_condition):
                if qty_of_one_stock > 0:
                    print(f" ******** Buying stocks for {symbol}... ")
                    print_technical_indicators(symbol, calculate_technical_indicators(symbol))
                    api_symbol = symbol.replace('-', '.')
                    buy_order = api.submit_order(
                        symbol=api_symbol,
                        qty=f"{qty_of_one_stock:.4f}",  # MODIFIED: Pass as string with 4 decimal precision
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                    print(f" {current_time_str}, Bought {qty_of_one_stock:.4f} shares of {api_symbol} at {current_price}")
                    with open(csv_filename, mode='a', newline='') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        csv_writer.writerow({
                            'Date': current_time_str,
                            'Buy': 'Buy',
                            'Quantity': round(qty_of_one_stock, 4),
                            'Symbol': api_symbol,
                            'Price Per Share': current_price
                        })
                    stocks_to_remove.append((api_symbol, current_price, today_date_str))
                    buy_stock_green_light = 1
                    order_filled = False
                    for _ in range(30):
                        order_status = api.get_order(buy_order.id)
                        if order_status.status == 'filled':
                            order_filled = True
                            break
                        time.sleep(2)
                    if order_filled and api.get_account().daytrade_count < 3:
                        stop_order_id = place_trailing_stop_sell_order(api_symbol, qty_of_one_stock, current_price)
                        if stop_order_id:
                            print(f"Trailing stop sell order placed for {api_symbol} with ID: {stop_order_id}")
                        else:
                            print(f"Failed to place trailing stop sell order for {api_symbol}")
                    else:
                        print(f"Buy order not filled or day trade limit reached for {api_symbol}")
                else:
                    print("Price increases are favorable, but quantity is 0. Not buying.")
                    buy_stock_green_light = 0
            else:
                print("Not buying based on technical indicators or price decreases.")
                print_technical_indicators(symbol, calculate_technical_indicators(symbol))
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred in buy_stocks: {str(e)}")
    try:
        with buy_sell_lock:
            for symbol, price, date in stocks_to_remove:
                bought_stocks[symbol] = (round(price, 4), date)
                stocks_to_buy.remove(symbol.replace('.', '-'))
                remove_symbol_from_trade_list(symbol.replace('.', '-'))
                trade_history = TradeHistory(
                    symbol=symbol,
                    action='buy',
                    quantity=round(qty_of_one_stock, 4),  # MODIFIED: Store fractional quantity
                    price=price,
                    date=date
                )
                session.add(trade_history)
                db_position = Position(
                    symbol=symbol,
                    quantity=round(qty_of_one_stock, 4),  # MODIFIED: Store fractional quantity
                    avg_price=price,
                    purchase_date=date
                )
                session.add(db_position)
            session.commit()
            refresh_after_buy()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {str(e)}")
    print("")
    print("Completed buy_stocks processing for all symbols.")
    print("")

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
            position = api.get_position(symbol)
            bought_price = float(position.avg_entry_price)
            qty = float(position.qty)  # MODIFIED: Use float for quantity
            open_orders = api.list_orders(status='open', symbol=symbol)
            if open_orders:
                print(f"There is an open sell order for {symbol}. Skipping sell order.")
                continue
            if current_price >= bought_price * 1.001:
                api.submit_order(
                    symbol=symbol,
                    qty=f"{qty:.4f}",  # MODIFIED: Pass as string with 4 decimal precision
                    side='sell',
                    type='market',
                    time_in_force='day'
                )
                print(f" {current_time_str}, Sold {qty:.4f} shares of {symbol} at {current_price} based on a higher selling price.")
                with open(csv_filename, mode='a', newline='') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    csv_writer.writerow({
                        'Date': current_time_str,
                        'Sell': 'Sell',
                        'Quantity': round(qty, 4),  # MODIFIED: Log fractional quantity
                        'Symbol': symbol,
                        'Price Per Share': current_price
                    })
                stocks_to_remove.append(symbol)
                time.sleep(2)
            time.sleep(2)
    try:
        with buy_sell_lock:
            for symbol in stocks_to_remove:
                del bought_stocks[symbol]
                trade_history = TradeHistory(
                    symbol=symbol,
                    action='sell',
                    quantity=round(qty, 4),  # MODIFIED: Store fractional quantity
                    price=current_price,
                    date=today_date_str
                )
                session.add(trade_history)
                session.query(Position).filter_by(symbol=symbol).delete()
            session.commit()
            refresh_after_sell()
    except SQLAlchemyError as e:
        session.rollback()

def place_trailing_stop_sell_order(symbol, qty_of_one_stock, current_price):
    try:
        stop_loss_percent = 1.0
        stop_loss_price = current_price * (1 - stop_loss_percent / 100)
        print(f"Attempting to place trailing stop sell order for {qty_of_one_stock:.4f} shares of {symbol} "
              f"with trail percent {stop_loss_percent}% (initial stop price: {stop_loss_price})")
        stop_order = api.submit_order(
            symbol=symbol,
            qty=f"{qty_of_one_stock:.4f}",  # MODIFIED: Pass as string with 4 decimal precision
            side='sell',
            type='trailing_stop',
            trail_percent=stop_loss_percent,
            time_in_force='gtc'
        )
        print(f"Successfully placed trailing stop sell order for {qty_of_one_stock:.4f} shares of {symbol} "
              f"with ID: {stop_order.id}")
        return stop_order.id
    except Exception as e:
        print(f"Error placing trailing stop sell order for {symbol}: {str(e)}")
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
        qty = float(position.qty)  # MODIFIED: Use float for quantity
        try:
            db_position = session.query(Position).filter_by(symbol=symbol).one()
            db_position.quantity = qty
            db_position.avg_price = avg_entry_price
            if POSITION_DATES_AS_YESTERDAY_OPTION and run_counter < 1:
                db_position.purchase_date = yesterday.strftime("%Y-%m-%d")
        except NoResultFound:
            purchase_date = yesterday if POSITION_DATES_AS_YESTERDAY_OPTION and run_counter < 1 else datetime.today()
            purchase_date_str = purchase_date.strftime("%Y-%m-%d")
            db_position = Position(symbol=symbol, quantity=qty, avg_price=avg_entry_price,
                                   purchase_date=purchase_date_str)
            session.add(db_position)
        bought_stocks[symbol] = (avg_entry_price, db_position.purchase_date)
    with open(run_counter_file, "w") as f:
        f.write(str(run_counter))
    session.commit()
    return bought_stocks

def load_positions_from_database():
    positions = session.query(Position).all()
    bought_stocks = {}
    for position in positions:
        symbol = position.symbol
        avg_price = position.avg_price
        qty = position.quantity  # MODIFIED: Quantity is already Float from database
        initial_api_returned_purchase_date = position.purchase_date
        purchase_date = initial_api_returned_purchase_date
        bought_stocks[symbol] = (avg_price, purchase_date)
    return bought_stocks

# [Unchanged main() function]
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
            print("------------------------------------------------------------------------------------")
            print("2024 Edition of the Bull Market Advanced Stock Market Trading Robot, Version 5 ")
            print("by https://github.com/CodeProSpecialist")
            print("------------------------------------------------------------------------------------")
            print(f"  {current_time_str} Cash Balance: ${cash_balance}")
            day_trade_count = api.get_account().daytrade_count
            print("\n")
            print(f"Current day trade number: {day_trade_count} out of 3 in 5 business days")
            print("\n")
            print("------------------------------------------------------------------------------------")
            print("\n")
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
                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
                print("Stocks to Purchase:")
                print("\n")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} ")
                    time.sleep(1)
                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
            if PRINT_ROBOT_STORED_BUY_AND_SELL_LIST_DATABASE:
                print_database_tables()
            if DEBUG:
                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
                print("Stocks to Purchase:")
                print("\n")
                for symbol in stocks_to_buy:
                    current_price = get_current_price(symbol)
                    atr_low_price = get_atr_low_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} | ATR low buy signal price: {atr_low_price}")
                print("\n")
                print("------------------------------------------------------------------------------------")
                print("\n")
                print("\nStocks to Sell:")
                print("\n")
                for symbol, _ in bought_stocks.items():
                    current_price = get_current_price(symbol)
                    atr_high_price = get_atr_high_price(symbol)
                    print(f"Symbol: {symbol} | Current Price: {current_price} | ATR high sell signal profit price: {atr_high_price}")
                print("\n")
            print("Do Not Stop this Robot or you will need to ")
            print("delete the trading_bot.db database file and start over again with an empty database. ")
            print("Placing trades without this Robot will also require ")
            print("deleting the trading_bot.db database file and starting over again with an empty database. ")
            print("")
            print("Waiting 60 seconds before checking price data again........")
            print("")
            time.sleep(60)
        except Exception as e:
            logging.error(f"Error encountered: {e}")
            time.sleep(120)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Error encountered: {e}")
        session.close()
