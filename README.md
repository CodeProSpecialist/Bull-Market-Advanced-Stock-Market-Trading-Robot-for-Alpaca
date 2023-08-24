******** Download the newest version of this Python Program today. Brand New Code today, 8-24-2023.    ********
Major software improvements, and increased stock trading activity. 

Introducing the Advanced Stock Market Trading Robot! 

Are you looking to trade electricity or utility stocks with unprecedented precision? Look no further! Our state-of-the-art trading robot harnesses the power of cutting-edge technologies to provide you with an unrivaled trading experience.

Key Features:

 Targeted Trading: Exclusively focuses on trading electricity and utility stocks, optimizing opportunities in this specific sector.
Real-time Insights: Downloads stock prices and carefully buys when the prices are low. 
The stocks sell for a profit when the price increases. 
 Thread-safe Execution: Uses threading and locks to ensure efficient and safe buy/sell operations.
Market Timing: Considers market open/close times, making sure trades are executed only during market hours.
Portfolio Management: Maintains your trading history and positions with the use of SQLAlchemy, allowing for seamless tracking and management. 
Alpaca API Integration: Built on top of the reliable Alpaca trading API for secure and robust execution.
Highly Configurable: Define your own stock list in a text file, giving you full control over your trading universe.
 Detailed Logging: Keeps a log of all buy and sell signals, helping you to analyze your trading performance.
Join the Future of Trading Today!
Whether you're a novice investor or a seasoned trader, 
our Advanced Stock Market Trading Robot can take your trading strategy to the next level. 
With its innovative features and focus on electricity and utility stocks, 
it's the perfect tool to navigate any market condition, including recessions.


Investing in the stock market involves risk, and past performance is not indicative of future results. 
Please consult with a financial professional before investing.

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
recession by buying only 1 share of a stock at a time. 
If you want to buy different quantities of stocks, then you can edit the 
python code. To buy 20 shares of stock, in 
the program section "def buy_stocks()", locate the buy order and change the buy order code qty= to look like qty=20 as shown below: 

if cash_available > current_price:
    api.submit_order(symbol=symbol, qty=20, side='buy', type='market', time_in_force='day')


This stock market robot works best if you purchase 25 to 30 different stocks at only 1 share per stock because the stocks are sold really soon when the price is at a profitable position to sell the stock. This Stock Trading Robot has a strategy to buy stocks today for selling tomorrow because this allows for much more stock trading activity to take place within the stock trading rules of day trading 3 maximum times in 5 business days. 

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


Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
