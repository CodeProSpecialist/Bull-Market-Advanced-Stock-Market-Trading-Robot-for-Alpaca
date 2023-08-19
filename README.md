***** Please download the newest version of this python program. 
This python program has been updated at 5:51pm, August 19, 2023. 


     This Python Stock Market Trading Bot has completely brand new, redesigned python 3 code today, August 19, 2023.
Proceed with caution because this python code is currently in beta testing mode. 

I needed to stop using the strict and somewhat buggy python Pandas Library to add more flexibility to the data frames. 
So, I am using talib and not using Pandas at all. 

This program will only work if you have 
at least 1 stock symbol in the electricity-or-utility-stocks-to-buy-list.txt 
because of the functionality of the python code to analyze stocks to buy 
at a future time. 

This stock market robot works best if you purchase 25 to 30 different stocks in fractional shares 
or at only 1 share per stock because the stocks are sold really soon when the price decreases. This Stock Trading Robot has a strategy to buy stocks today for selling tomorrow because this allows for much more stock trading activity to take place within the stock trading rules of day trading 3 maximum times in 5 business days. 

Buying stocks during the 2023 Recession is not easy for anyone: not even easy for computers and robots. 

      The event of the 2023 recession means trouble for your "unprepared" investment portfolio. 
   The economy is contracting, markets are falling and risky assets are losing value. 
   At times like these, experienced investors rotate 
   into recession stocks that perform well—or lose less value—during an economic contraction. 

Recession stocks are defensive stocks that can sustain growth or 
limit their losses during an economic downturn because their products are always in demand. 
The best recession stocks include consumer staples, utilities and healthcare companies, 
all of which produce goods and services that consumers can’t do without, no matter how bad the economy gets.
 Extremely important: invest in Electricity, Natural Gas, and perhaps even Crude Oil stocks. 
  Some Energy stocks include: XLE, XOM, AEE, CMS, PCG, EQT, SLB, and CVX. 
   
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

Let's break down the code to understand its working step by step. This code appears to be part of a stock trading bot specifically for electricity or utility stocks. Here's a detailed explanation:
1. Initialization and Environment Variables

    Import Modules: The necessary libraries for logging, datetime operations, trading APIs, etc., are imported.
    Alpaca API Initialization: Alpaca's trading API is initialized using environment variables for API keys and base URL.
    Timezone Setting: Eastern Time is used, as it corresponds to the New York Stock Exchange's time zone.

2. Functions Defined

    stop_if_stock_market_is_closed(): This function checks whether the stock market is open or not. If closed, it waits in a loop and prints a waiting message until the market opens.

    get_stocks_to_trade(): Reads a list of stock symbols (electricity or utility stocks) from a file.

    get_current_price(symbol): Fetches the current closing price of a given stock symbol.

    get_atr_high_price(symbol): Calculates a high price based on the Average True Range (ATR) and current price.

    get_average_true_range(symbol): Calculates the Average True Range (ATR) for a given symbol.

3. Main Logic
3.1 Checking Market Hours

    The main loop of the code first calls stop_if_stock_market_is_closed(), which makes the program wait if the market is closed.

3.2 Buying Stocks

    The code then gets the current time and cash balance.
    It checks if the time is 3:50 pm (15:50 Eastern Time). If so, it iterates through the stocks to trade.
    For each stock, it calculates a "fractional quantity" based on the available cash and current price.
    If enough cash is available, it submits a buy order for that fractional quantity and stores the current price in the bought_stocks dictionary.

3.3 Selling Stocks

    For each bought stock, the code checks the current price and calculates the ATR high price.
    If the current price is greater than or equal to the ATR high price, it fetches the quantity of that stock held and submits a sell order.
    The sold stock is removed from the bought_stocks dictionary.

3.4 Time Sleep

    The code then sleeps for 2 seconds before starting the next iteration.

4. Exception Handling

    If an exception is encountered in the main function, it's logged, and the program sleeps for 2 seconds before continuing.

Summary

The code effectively manages a trading bot for electricity or utility stocks, making buying decisions at a specific time, and selling based on calculated ATR high price. The bot continues to run, constantly checking the market hours and performing buying or selling actions as necessary.

Please note that this script is designed to run during the stock market's operating hours. 

This Advanced Stock Market Robot seems to be working great. 
Important note: This Stock Market Robot will quickly sell any stocks 
that decrease in value, sometimes even selling just by 1 percent to prevent losing any money 
at all during the 2023 Stock Market Recession. 

Important Instructions: 
     To buy and sell stocks, run the python script named buy-and-automatically-sell-for-a-profit-robot.py 
with the command: python3 buy-and-automatically-sell-for-a-profit-robot.py 
 Place this program into "buy more stocks mode" 
 when you put stock symbols in the text file "electricity-or-utility-stocks-to-buy-list.txt"
 and the stock market trading robot keeps looking for chances to buy more stocks
 from the list of stock symbols.

   I also recommend to not select stocks that are valued less than 200 dollars to have the stocks work well 
with this stock bot because it is more worth your time to use your single or last few day trades 
to generate a larger dollar amount of profit from a 2 percent profit before the stock is sold. 
I also recommend only having this stock bot monitor your favorite stock that you have 
noticed increasing in price numbers. This will make this stock bot generate the most profit for 
you in the least amount of time. 

Advanced Stock Market Trading Bot

This is a stock market portfolio management application that helps minimize losses and maximize profits.
This works with the Alpaca stock market trading broker. 
Advanced Stock Market Trading Bot only works Monday through Friday: 9:30am - 4:00pm Eastern Time.

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

Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
