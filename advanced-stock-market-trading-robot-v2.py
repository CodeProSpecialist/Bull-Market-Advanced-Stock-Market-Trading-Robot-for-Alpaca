import os
import time
from datetime import datetime
import pytz
import alpaca_trade_api as tradeapi
import yfinance as yf
import talib

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
            print(f"Day Trade Count: {account.daytrade_count} out of 3 maximum per 5 days. ")

            print("\nPositions:")
            for position in positions:
                print(f"Symbol: {position.symbol}, Quantity: {position.qty}, Avg Entry Price: {float(position.avg_entry_price):.2f}")

            print("\nCurrent Prices:")
            for symbol, price in prices.items():
                print(f"Symbol: {symbol}, Price: {price:.2f}")

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
        # We are using Moving Average Convergence Divergence (MACD), Relative Strength Index (RSI), and Bollinger Bands as indicators for buying signals
        bars = yf.download(symbol, period="1mo")
        close_prices = bars['Close']
        macd, macdsignal, macdhist = talib.MACD(close_prices)
        rsi = talib.RSI(close_prices)
        upper, middle, lower = talib.BBANDS(close_prices)

        # Generate signals based on the indicators
        macd_signal = macd[-1] > macdsignal[-1]  # MACD crosses above signal line
        rsi_signal = rsi[-1] < 30  # RSI is below 30 (Oversold)
        bollinger_signal = close_prices[-1] < lower[-1]  # Price crosses below lower Bollinger Band

        return macd_signal and rsi_signal and bollinger_signal

    def bearish(self, symbol):
        # Place your logic here for bearish signal
        # We are using Moving Average Convergence Divergence (MACD), Relative Strength Index (RSI), and Bollinger Bands as indicators for selling signals
        bars = yf.download(symbol, period="1mo")
        close_prices = bars['Close']
        macd, macdsignal, macdhist = talib.MACD(close_prices)
        rsi = talib.RSI(close_prices)
        upper, middle, lower = talib.BBANDS(close_prices)

        # Generate signals based on the indicators
        macd_signal = macd[-1] < macdsignal[-1]  # MACD crosses below signal line
        rsi_signal = rsi[-1] > 70  # RSI is above 70 (Overbought)
        bollinger_signal = close_prices[-1] > upper[-1]  # Price crosses above upper Bollinger Band

        return macd_signal and rsi_signal and bollinger_signal

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
        bars = yf.download(symbol, period="1d")
        price = bars['Close'].iloc[-1]

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
            time_in_force='day'
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
                    time_in_force='day'
                )
                print(f"Submitted order to sell all shares of {position.symbol}")

        def get_current_prices(self):
            prices = {}

            for symbol in self.symbols:
                ticker = yf.Ticker(symbol)
                price = ticker.history(period="1d")['Close'].iloc[-1]
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
