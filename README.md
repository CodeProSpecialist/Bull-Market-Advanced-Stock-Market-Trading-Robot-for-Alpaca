***** Please download the newest version of this python program. 
The program code had some bugs removed. Some errors were fixed. 
This python program has been updated on August 20, 2023. *****


     This Python Stock Market Trading Bot has completely brand new, redesigned python 3 code. 
Proceed with caution because this python code is currently in beta testing mode, although 
this Python 3 code has successfully passed numerous software experimental tests to determine that this stock market trading robot is ready to accomplish more amazing work. 
An Advanced Artificial Intelligence Software 
platform has analyzed this Python 3 code to 
be designed, functional, and working 
correctly. 

I needed to stop using the strict and somewhat buggy python Pandas Library to add more flexibility to the data frames. 
So, I am using talib and not using Pandas at all. 

***** This program will only work if you have 
at least 1 stock symbol in the electricity-or-utility-stocks-to-buy-list.txt 
because of the functionality of the python code to analyze stocks to buy 
at a future time. Otherwise, you will most likely see errors in the log-file-of-buy-and-sell-signals.txt. *****

You can modify the python script to make DEBUG = True   and this will print out your stocks with the price information. 
Printing out the stock information slows down this python program, and it is recommended to change debug back to:  
DEBUG = False

Use a python code IDE like Pycharm to edit 
this python code. 

This python code is currently programmed to 
spend less money during a stock market 
recession by buying only stocks that can 
be purchased in fractional shares. 
If you want to buy stocks that can only 
be purchased at full price, then in 
the program section "def buy_stocks()", locate the buy order and change the buy order code qty= to look like qty=1 as shown below: 

if cash_available > current_price:
    api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='day')


This stock market robot works best if you purchase 25 to 30 different stocks in fractional shares 
or at only 1 share per stock because the stocks are sold really soon when the price decreases. This Stock Trading Robot has a strategy to buy stocks today for selling tomorrow because this allows for much more stock trading activity to take place within the stock trading rules of day trading 3 maximum times in 5 business days. 

Any stocks purchased today will not begin to sell until tomorrow or until a future day when the stock price increases during stock market 
trading hours, Monday through Friday. 

Buying stocks during the 2023 Recession is not easy for anyone: not even easy for computers and robots. 

      The event of the 2023 recession means trouble for your "unprepared" investment portfolio. 
   The economy is contracting, markets are falling and risky assets are losing value. 
   At times like these, experienced investors rotate 
   into recession stocks that perform well—or lose less value—during an economic contraction. 

Recession stocks are defensive stocks that can sustain growth or 
limit their losses during an economic downturn because their products are always in demand. 
The best recession stocks include consumer staples, utilities and healthcare companies, 
all of which produce goods and services that consumers can’t do without, no matter how bad the economy gets.
 Extremely important: invest in Electricity and Natural Gas stocks.  
  Some Energy stocks include: VST, PCG, NEE, SO, DUK, NEE-PR, 
  NGG, AEP, D, EXC, WEC, AWK, EIX, ES, and DTE. 
   
   In the ever-changing world of the stock market, opportunity can rise and fall in an instant...

That's why we've developed the ultimate tool to help you seize the moment and maximize your profits. 

Meet your new ally, the state-of-the-art, Advanced Stock Market Day Trading Robot. 

Harnessing the power of cutting-edge Python 3 programming code and sophisticated financial algorithms, 

our Day Trading Robot is designed to operate with precision and speed that's beyond human capabilities. 

It leverages the renowned Average True Range Indicator for reliable price signals that can be utulized to trade stocks at the best price possible.  

It's programmed in Python 3 to analyze market data at lightning speed, 

monitoring multiple stocks simultaneously for optimal trade execution.

Getting started is as easy as a few clicks. Just load your stock list, set up your Alpaca trade API keys, 

and let the Robot do the heavy lifting. 

Our Robot is proactive and smart, making trades when the time is right, 

and holding back when it's not, ensuring you're on the right path to growing your portfolio. 

With our Day Trading Robot, the future of profitable, stress-free trading is here. 

Embrace the technology and let the Robot do the trading. 

Advanced Stock Market Day Trading Robot – Trading Simplified. 

Remember, the success in trading stocks and other securities can never be guaranteed. 
Please trade responsibly and do your own research before making any investment. 
This does not constitute financial advice.

Below is an analysis of the given code, detailing the purpose and functionality of each part:
Import Statements

    Various modules are imported to facilitate date and time handling, logging, 
    and to interface with Alpaca's trading API and other financial tools.

Global Variables and API Initialization

    Environment variables are loaded to configure the Alpaca API.
    The Alpaca API is initialized for trading actions.
    A timezone (eastern) is defined, and a global dictionary (stock_data) is initialized for storing stock information.

stop_if_stock_market_is_closed()

    This function runs an infinite loop, checking if the current time is within the stock market's open hours.
    If the market is closed, a message is printed and the program sleeps for one minute before checking again.

Logging Configuration

    Configures logging to write buy and sell signals to a file.

get_stocks_to_trade()

    Reads a file containing a list of electricity or utility stocks to buy and returns them as a list.

remove_symbol_from_trade_list(symbol)

    Removes a given stock symbol from the list of stocks to buy in the file.

get_current_price(symbol)

    Retrieves the current closing price of a given stock symbol. 

get_atr_high_price(symbol) and get_atr_low_price(symbol)

    Calculate and return the high and low price levels for a given symbol based on the Average True Range (ATR), using the TA-Lib library.

get_average_true_range(symbol)

    Calculates the Average True Range (ATR) of a given stock symbol for the past 30 days.

save_bought_stocks_to_file(bought_stocks) and load_bought_stocks_from_file()

    These functions save and load the details of bought stocks to and from a file, including the symbol, price, and purchase date.

update_bought_stocks_from_api()

    Retrieves the details of bought stocks from the Alpaca API and saves them to a file.

main()

    The main function orchestrates the trading logic:
        Loops indefinitely, executing the trading logic.
        Calls stop_if_stock_market_is_closed() to ensure trading only during market hours.
        Retrieves the list of stocks to buy and the details of bought stocks.
        Iterates through the stocks to buy, placing buy orders if conditions are met, and updating the list of bought stocks.
        Checks for sell conditions based on ATR and sells if conditions are met.
        Handles exceptions and logs errors.

if __name__ == '__main__':

    Executes the main() function if the script is run as the main program, and handles exceptions at the top level.

Summary

The code represents a stock trading bot specifically designed to trade electricity or utility stocks. 
It follows specific buy and sell strategies based on price and Average True Range (ATR), 
and it ensures that trading only happens during market hours. 
The code interacts with the Alpaca API for trading actions and uses other libraries for financial data analysis. 
It also maintains logs and handles files for storing the list of stocks to trade and the details of bought stocks.

Advanced Stock Market Trading Bot


This is an Advanced buying and selling Python 3 Trading Robot 
to monitor a stock market symbol or a number of stock symbols that you place in the file "electricity-or-utility-stocks-to-buy-list.txt". 
Only place one stock symbol on each line. 
 

To install:

Do not be the root user. This installs from a regular user account. 
***** The below install commands are ONLY for a Desktop or Laptop Computer x86_64 type of install. ***** 
Open a command line terminal from this folder location and type: 

sh install.sh

After placing your alpaca keys at the bottom of /home/nameofyourhomefolderhere/.bashrc you simply run the command in a command terminal like:

python3 buy-and-automatically-sell-for-a-profit-robot.py 

Make sure to not modify or edit the file named stock-database.txt because 
it is storing information to remember when the program is working. 

Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
