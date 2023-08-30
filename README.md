********* Download the newest version of this Python program. 
Major software update on 8-29-2023 *********
  
  Welcome to the Future of Trading with the Advanced Stock Market Trading Robot!

Why Trade Manually When You Can Automate It? 

Introducing the 2023 Edition of the Advanced Stock Market Trading Robot, specially designed to help you take your trading game to the next level! This state-of-the-art trading algorithm is powered by Python, and it's packed with amazing features that you'll love:

    Alpaca API Integration: Trade with confidence and speed using the reliable Alpaca API.
    Smart Buy/Sell Strategies. 
    Thread-Safe Operations: Utilizing threading and locks to ensure smooth concurrent operations.
    SQLAlchemy Database Support: Keep track of all your positions and trade history with a robust SQLite database.
    Debugging and Database Printing: Want insights into what's happening behind the scenes? 
    Toggle the DEBUG and PRINT_DATABASE options to see the stored database information print out. 

But Wait, There's More!

DEBUG Mode
Tired of guessing what's happening inside your trading robot? Activate DEBUG mode, and you'll get a detailed look into the stocks you're planning to purchase and sell, along with their ATR-derived buy and sell prices. It's like having X-ray vision for your trades!

PRINT_DATABASE Option
Curious about your trading history or current positions? Turn on PRINT_DATABASE, and you'll see the entire Trade History and Positions tables printed right in your console! It's your trading journey at a glance!

Market Hours Monitoring
Never worry about trading out of hours. The bot knows when the market is open and ensures that it only trades during those times.

Easy Customization
Manage your stock selection by simply updating the 'electricity-or-utility-stocks-to-buy-list.txt' file. It's that simple!

Logging
Keep track of buy and sell signals with detailed logging. Every move is recorded, so you're never in the dark.

Educational
Learn from the code! The well-documented functions and clear structure make this a fantastic learning opportunity for aspiring traders and Python enthusiasts alike.

Join the trading revolution today with the Advanced Stock Market Trading Robot! 
Clone the code, set your API keys, and let the robot do the trading for you. It's time to trade like it's 2023!


Disclaimer: This software is not affiliated or endorsed by Alpaca Securities, LLC. 
Always do your own research before investing. Investing in the stock market involves risk, and past performance is not indicative of future results. 
Please consult with a financial professional before investing. 

Happy Trading. 


***** This program will only work if you have 
at least 1 stock symbol in the electricity-or-utility-stocks-to-buy-list.txt 
because of the functionality of the python code to analyze stocks to buy 
at a future time. Otherwise, you will most likely see errors in the log-file-of-buy-and-sell-signals.txt. A new database file will need to be created if you started this robot without owning any stocks. Delete the database file named trading_bot.db before restarting the stockbot if the stockbot was running without any owned stock positions. 
Stop and Start the Stock Trading Robot after you have purchased at least 1 share of stock to create a new database file.   *****

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
the program section "def buy_stocks()", locate qty_of_one_stock = 1 and change the buy order code qty_of_one_stock to look as shown below: 

qty_of_one_stock = 20


This stock market robot works best if you purchase 25 to 30 different stocks at only 1 share per stock because the stocks are sold really soon when the price is at a profitable position to sell the stock. This Stock Trading Robot has a strategy to buy stocks today for selling tomorrow because this allows for much more stock trading activity to take place within the stock trading rules of day trading 3 maximum times in 5 business days. 

Any stocks purchased today will not begin to sell until tomorrow or until a future day when the stock price increases during stock market 
trading hours, Monday through Friday. 


This is an Advanced buying and selling Python 3 Trading Robot 
to monitor a stock market symbol or a number of stock symbols that you place in the file "electricity-or-utility-stocks-to-buy-list.txt". 
Only place one stock symbol on each line. 
 

To install:

You should be the root user when installing the Python software. 
***** The below install commands are ONLY for a Desktop or Laptop Computer x86_64 type of install. ***** 
Open a command line terminal from this folder location and type: 

sh install.sh

Do the following with a non-root user account: 
After placing your alpaca keys at the bottom of /home/nameofyourhomefolderhere/.bashrc you simply run the command in a command terminal like:

python3 buy-and-automatically-sell-for-a-profit-robot.py 


Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
