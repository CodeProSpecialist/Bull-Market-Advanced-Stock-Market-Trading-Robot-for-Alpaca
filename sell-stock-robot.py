import alpaca_trade_api as tradeapi
from datetime import datetime
from datetime import time as time2
import time
import pytz
import os

# Initialize the Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

def introduction():
    print("Welcome to the Stock Selling Program that sells your Alpaca Stock Shares. ")
    print("This program will sell all shares of a specific stock symbol at a specified price. ")
    print("You will set a target price, and the program will monitor the price to sell when it decreases by 1 penny. ")
    print("If the price increases above the target by 1 penny, a new stop loss flag will be triggered. ")
    print("This allows the price to increase to its maximum and then sell immediately if it drops by 1 penny. ")
    print("--------------------")

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
        print("Stockbot only works Monday through Friday: 9:30 am - 4:00 pm Eastern Time.")
        print("Waiting until Stock Market Hours to begin the Stockbot Trading Program.")
        time.sleep(60)  # Sleep for 1 minute and check again


def sell_stock(symbol, target_price):
    while True:
        # Get current positions
        positions = api.list_positions()
        owned_positions = [position for position in positions if position.symbol == symbol]

        # Check if we own any positions for the given symbol
        if not owned_positions:
            print(f"You don't own any shares of {symbol}. Exiting the program.")
            return

        # Calculate the total quantity of shares and average price for the given symbol
        total_qty = sum([float(position.qty) for position in owned_positions])
        current_price = sum([float(position.current_price) for position in owned_positions]) / len(owned_positions)

        # Print the current date and time in Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        print(f'Current date & time (Eastern Time): {now.strftime("%A, %B %d, %Y, %H:%M:%S")} ')
        print(f"Symbol: {symbol}, Current Stock Market Price: ${current_price:.2f}")
        print("--------------------")
        print(f"Stock Symbol to Sell: {symbol}")
        print(f"Target Sell Price: ${target_price:.2f}\n")

        # Check if the target price is reached or exceeded
        if current_price >= target_price:
            print(f"Target price of ${target_price:.2f} reached for {symbol}.")
            print(f"Selling all {total_qty} shares of {symbol} at an average price of ${current_price:.2f}.")
            if total_qty > 0:
                api.submit_order(
                    symbol=symbol,
                    qty=total_qty,
                    side="sell",
                    type="market",
                    time_in_force="day"  # Set the order type to "day"
                )
                print("All shares sold successfully.")
            break

        # Wait for 1 second before checking the price again
        time.sleep(1)


def main():
    # Check if the stock market is closed
    stop_if_stock_market_is_closed()

    # Read target price from the text file
    with open("sell-stocks-price.txt", "r") as f:
        target_price = float(f.read())

    # Read stock symbol from the text file
    with open("the-stock-symbol-to-sell.txt", "r") as f:
        symbol = f.read().strip().upper()

    introduction()

    # Print the stock symbol and target price
    print(f"Stock Symbol to Sell: {symbol}")
    print(f"Target Sell Price: ${target_price:.2f}\n")

    # Sell the stock based on the specified target price and stop loss conditions
    sell_stock(symbol, target_price)

    # Sleep for 10 minutes after selling the stock
#    print("Sleeping for 10 minutes before exiting the program.")
#    time.sleep(600)  # Sleep for 10 minutes

if __name__ == "__main__":
    main()
