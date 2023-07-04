import alpaca_trade_api as tradeapi
from datetime import datetime
import pytz

class AlpacaBot:
    def __init__(self, symbols):
        self.api = tradeapi.REST('<Alpaca Key ID>', '<Alpaca Secret Key>', base_url='https://paper-api.alpaca.markets')
        self.symbols = symbols

    def run(self):
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        print(f"Current Eastern Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        if not self.is_market_open():
            print("Waiting for the stock market to open to begin working.")
            return

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

            self.buy_signals()
            self.sell_signals()

            # Sleep for 1 minute before the next iteration
            time.sleep(60)

    def is_market_open(self):
        clock = self.api.get_clock()
        return clock.is_open

    def bullish(self, symbol):
        # Place your logic here for bullish signal
        return False

    def bearish(self, symbol):
        # Place your logic here for bearish signal
        return False

    def get_market_cap(self, symbol):
        asset = self.api.get_asset(symbol)
        return asset.market_cap

    def calculate_RSI(self, symbol):
        # Place your logic here for RSI calculation
        return 0

    def moving_volume(self, symbol):
        # Place your logic here for moving volume calculation
        return 0

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
        barset = self.api.get_barset(symbol, "day", limit=1)
        bar = barset[symbols][0]
        price = bar.c

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

        barsets = self.api.get_barset(','.join(self.symbols), "minute", limit=1)
        for symbol in self.symbols:
            bars = barsets[symbol]
            if bars:
                price = bars[0].c
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
