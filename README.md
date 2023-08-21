Introduction:
Welcome to the ultimate stock trading robot, designed exclusively for navigating the dynamic world of electricity stocks during recession market conditions! Harnessing the power of cutting-edge Python programming, financial analytics, and smart trading strategies, this trading robot takes your stock market journey to the next level. Say goodbye to manual trading and let automation guide your stock decisions with precision.

Analysis:
In today's volatile market, having a trading companion that can think and act faster than any human is essential. This Python-powered stock trading robot leverages the prowess of several Python libraries and APIs to automate trading activities and maximize profits. Developed with a focus on electricity stocks, this robot adapts to recession market conditions to optimize your trading portfolio.

Key Features:

    Real-Time Data Analysis: The robot taps into the Alpaca API to fetch real-time market data, ensuring you're always one step ahead of the competition.

    Smart Buying and Selling: Powered by artificial intelligence, the robot employs sophisticated algorithms to identify the best entry and exit points, optimizing your profits while minimizing risks.

    Automated Decision-Making: No need to watch the market all day. The robot operates autonomously, making informed trading decisions based on data-driven analysis.

    Risk Management: By considering Average True Range (ATR), the robot sets dynamic price thresholds for buying and selling, adapting to market fluctuations and ensuring prudent risk management.

    Data Storage: The robot maintains a detailed record of bought and sold stocks in a secure SQLite database, ensuring transparency and accountability.

In-Depth Review:
This Python script is designed to create an automated stock trading experience tailored to the challenging world of electricity stocks during a market recession. The script is powered by several key components and libraries, each contributing to its functionality and effectiveness.

1. Data Collection and Analysis:
The script relies on the Alpaca API to gather real-time market data, enabling it to make timely and accurate decisions. The use of the alpaca_trade_api library ensures seamless communication with the Alpaca trading platform.

2. AI-Enhanced Trading Strategy:
The script implements advanced trading strategies guided by artificial intelligence. It calculates the Average True Range (ATR) for each stock to set dynamic buying and selling thresholds. This approach ensures that the robot adapts to changing market conditions and avoids making impulsive decisions.

3. Buy and Sell Mechanisms:
The robot operates in a multi-threaded environment, with separate threads for buying and selling. The buy_stocks() function uses a lock to ensure synchronized buying decisions, considering available cash balance and stock prices. The sell_stocks() function follows a similar pattern for selling decisions.

4. Database Integration:
The robot maintains a SQLite database named stocks.db to keep track of bought and sold stocks. The initialize_database() function sets up the database structure, and the save_bought_stocks_to_database() and load_bought_stocks_from_database() functions manage data storage and retrieval.

5. Continuous Operation:
The script runs in an infinite loop, continuously monitoring market conditions and making trading decisions. It also provides valuable information about cash balance, day trade count, and the list of stocks to buy and sell.

6. Error Handling and Logging:
To ensure robust performance, the script includes error handling mechanisms. It logs errors to a text file named log-file-of-buy-and-sell-signals.txt, allowing for easy debugging and troubleshooting.

Conclusion:
With its blend of real-time data analysis, AI-driven strategies, and automated execution, this Python stock trading robot is your ideal companion in navigating the challenging landscape of electricity stocks during a market recession. Embrace the future of trading and enhance your portfolio's performance with this powerful and intelligent tool.

Disclaimer:
Trading in the stock market involves risks and uncertainties. The performance of the trading robot is based on historical data and past performance, and there is no guarantee of future results. Make sure to thoroughly research and understand the trading strategies implemented in the script before using it for real trading activities.

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

There is a known situation where this program will not work until you buy at least 1 share of stock 
or a fractional share of stock because when this program starts running, it needs at least 1 stock 
to save in the database to create a new database. That is just how databases work and there is really 
no other way around creating a new database with at least 1 stock symbol to add to the database. 
 A database needs to be created when this Stock Market Robot begins working 
to keep track of all of the stock position buying and selling. 
Thanks for understanding. Stocks can be purchased at the Alpaca website. 
This software is not affiliated or endorsed by Alpaca Securities, LLC 
This software does, however try to be a useful, profitable, 
and valuable stock market trading application.
   
Make sure to not modify or edit the file named stocks.db because 
it is storing information to remember when the program is working. It is a professional database file. 

Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
