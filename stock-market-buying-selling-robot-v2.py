import alpaca_trade_api as tradeapi
from datetime import datetime
import pytz
import time
import os
import yfinance as yf

APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

class AlpacaBot:
    def __init__(self, symbols):
        self.api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
        self.symbols = symbols

    def run(self):
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        print(f"Current Eastern Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        while True:
            account = self.api.get_account()
            positions = self.api.list_positions()
            prices = self.get_current_prices()

            print("\nAccount Information:")
            print(f"Current account cash: {account.cash}")
            print(f"Day Trade Count: {account.daytrade_count}")

            print("\nPositions:")
            for position in positions:
                print(f"Symbol: {position.symbol}, Quantity: {position.qty}, Avg Entry Price: {position.avg_entry_price}")

            print("\nCurrent Prices:")
            for symbol, price in prices.items():
                print(f"Symbol: {symbol}, Price: {price}")

            if self.is_market_open():
                self.buy_signals()
                self.sell_signals()
            else:
                print("Waiting for the stock market to open.")

            # Sleep for 1 minute before the next iteration
            time.sleep(60)

    def is_market_open(self):
        clock = self.api.get_clock()
        return clock.is_open

    def bullish(self, symbol):
        # Place your logic here for bullish signal
        # Example: Check if the stock's price is above a certain moving average
        # You can add your own conditions based on your trading strategy
        ticker_info = yf.Ticker(symbol)
        history = ticker_info.history(period="1d")
        moving_average = history['Close'].mean()
        current_price = history.iloc[-1]['Close']
        
        return current_price > moving_average

    def bearish(self, symbol):
        # Place your logic here for bearish signal
        # Example: Check if the stock's price is below a certain moving average
        # You can add your own conditions based on your trading strategy
        ticker_info = yf.Ticker(symbol)
        history = ticker_info.history(period="1d")
        moving_average = history['Close'].mean()
        current_price = history.iloc[-1]['Close']
        
        return current_price < moving_average

    def get_market_cap(self, symbol):
        asset = self.api.get_asset(symbol)
        return asset.market_cap

    def calculate_RSI(self, symbol):
        # Place your logic here for RSI calculation
        # Example: Calculate the RSI using historical price data
        # You can add your own calculation method based on your trading strategy
        ticker_info = yf.Ticker(symbol)
        history = ticker_info.history(period="1d")
        price_changes = history['Close'].diff().dropna()

        up_moves = price_changes[price_changes > 0]
        down_moves = price_changes[price_changes < 0]

        avg_up = up_moves.mean()
        avg_down = abs(down_moves.mean())

        relative_strength = avg_up / avg_down
        rsi = 100 - (100 / (1 + relative_strength))

        return rsi

    def buy_signals(self):
        for symbol in self.symbols:
            # Get the current account info
            account = self.api.get_account()

            # Parse the string to get the cash as a float
            cash = float(account.cash)

            if self.bullish(symbol):
                self.buy_stock(symbol, cash)

    def sell_signals(self):
        account = self.api.get_account()
        positions = self.api.list_positions()

        for position in positions:
            if self.bearish(position.symbol):
                self.sell_stock(position)

    def buy_stock(self, symbol, cash):
        # Get account and check day trade count
        account = self.api.get_account()
        if account.daytrade_count >= 3:
            print("Day trade limit reached. Not buying.")
            return

        # Get the last closing price of the stock
        ticker_info = yf.Ticker(symbol)
        history = ticker_info.history(period="1d")
        price = history.iloc[-1]['Close']

        # Calculate the maximum number of shares we can buy
        num_shares = int(cash / price)

        # If we can't buy at least 1 share, then don't submit the order
        if num_shares < 1:
            print(f"Not enough cash to buy a single share of {symbol}")
            return

        # Submit the order
        self.api.submit_order(
            symbol=symbol,
            qty=num_shares,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Submitted order to buy {num_shares} shares of {symbol}")

    def sell_stock(self, position):
        # Get account and check day trade count
        account = self.api.get_account()
        if account.daytrade_count >= 3:
            print("Day trade limit reached. Not selling.")
            return

        if position.qty > 0:
            # Submit an order to sell all shares of this stock
            self.api.submit_order(
                symbol=position.symbol,
                qty=position.qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Submitted order to sell all shares of {position.symbol}")

    def get_current_prices(self):
        prices = {}

        for symbol in self.symbols:
            ticker_info = yf.Ticker(symbol)
            price = ticker_info.history(period="1d").iloc[-1]['Close']
            prices[symbol] = price

        return prices


if __name__ == "__main__":
    symbols = []
    while True:
        symbol = input("Enter a stock symbol (or 'exit' to finish): ")
        if symbol == "exit":
            break
        symbols.append(symbol)

    print("\nSymbols Entered:")
    for i, symbol in enumerate(symbols, 1):
        print(f"{i}. {symbol}")

    while True:
        print("\nMenu:")
        print("1. Continue")
        print("2. Edit Symbol")
        choice = input("Select an option: ")

        if choice == "1":
            break
        elif choice == "2":
            print("\nEdit Symbol:")
            for i, symbol in enumerate(symbols, 1):
                print(f"{i}. {symbol}")

            symbol_number = int(input("Enter the symbol number to edit: "))
            if symbol_number in range(1, len(symbols) + 1):
                new_symbol = input("Enter the new symbol: ")
                symbols[symbol_number - 1] = new_symbol
            else:
                print("Invalid symbol number. Please try again.")
        else:
            print("Invalid option. Please try again.")

    bot = AlpacaBot(symbols)
    bot.run()
