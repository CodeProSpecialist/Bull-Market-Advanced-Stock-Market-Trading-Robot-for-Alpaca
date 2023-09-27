******** There is currently a known datetime error message that is being worked on to remove. You can ignore the error message because this Stock Trading Robot is still functioning really well without any problems. Just make sure to download the newest version of this Stock Trading Robot from week to week until this message is deleted from the README file. Thanks for understanding.  ********





-----------------------------------------------------------------------------------------------
        Welcome to the Future of Trading with the Advanced Stock Market Trading Robot! 

                    Why Trade Manually When You Can Automate It? 

        Introducing the 2023 Edition of the Advanced Stock Market Trading Robot, Version 2  
-----------------------------------------------------------------------------------------------

![Screenshot-1](https://github.com/CodeProSpecialist/Advanced-Stock-Market-Trading-Bot-Version-2-for-Alpaca/assets/111866070/c9f0bfb9-f964-440d-a208-e520ef30e0d5)

![Screenshot-2](https://github.com/CodeProSpecialist/Advanced-Stock-Market-Trading-Bot-Version-2-for-Alpaca/assets/111866070/f3ac8445-3c3d-492d-b9d8-83c602714202)

![image](https://github.com/CodeProSpecialist/Advanced-Stock-Market-Trading-Bot-Version-2-for-Alpaca/assets/111866070/a055ae45-bf3e-4dde-8084-11afcbe26cc1)

![Screenshot-3](https://github.com/CodeProSpecialist/Advanced-Stock-Market-Trading-Bot-Version-2-for-Alpaca/assets/111866070/65a4ce80-4470-4bd9-a5a2-4c9d0eff3155)

![Screenshot-4](https://github.com/CodeProSpecialist/Advanced-Stock-Market-Trading-Bot-Version-2-for-Alpaca/assets/111866070/aa3e467a-2d67-44d4-afbf-495d5e24cf50)


 Are you ready to take your stock trading game to the next level? The Advanced Stock Market Trading Robot is here to help you navigate the complexities of the stock market and make informed trading decisions. This cutting-edge trading software is designed to excel in recession market conditions, focusing exclusively on electric utility and energy stocks. 

Stock Robot

Key Features:

  Real-Time Trading: Our robot operates during stock market hours, ensuring you never miss an opportunity. It's designed to work efficiently and effectively, making the most of your trading time.

  Data-Driven Insights: We leverage powerful data analysis tools like Python 3 SQLAlchemy, and Talib to provide you with accurate and timely information for your trading decisions. 

  Lock and Load: With built-in thread locking mechanisms, you can buy and sell stocks in parallel without worrying about conflicts or errors. Your trades will execute smoothly.

  Detailed Logging: Every trade and decision is meticulously logged, so you can review your trading history and learn from your past experiences.

How It Works:

   Prepare Your List: Add your preferred electricity stocks to the "electricity-or-utility-stocks-to-buy-list.txt" file. This is your watchlist.

    Set Up: Ensure you have your Alpaca API credentials (API Key ID and API Secret Key) ready. These will be used to interact with the market.

   Run the Robot: Start the robot using the "buy-and-automatically-sell-for-a-profit-robot.py" script. It will automatically buy and sell stocks based on your criteria.

   Monitoring: The robot will continuously monitor the market, buying stocks meeting your criteria and selling when the conditions are right.

    Review: Keep an eye on your trades and positions. The robot logs all actions, providing you with a clear picture of your trading history. 

Stay In Control:

The Advanced Stock Market Trading Robot is designed to work with stocks you already own. It won't initiate new positions unless you specify them in your watchlist. This ensures you maintain control over your portfolio.

  The 2023 Edition of the Advanced Stock Market Trading Robot, specially designed to help you take your trading game to the next level! This state-of-the-art trading algorithm is powered by Python, and it's packed with amazing features that you'll love:

1. Parallel Execution: The "buy_stocks" function runs in parallel with the main program, allowing it to continuously monitor and purchase stocks.

2. Stock Selection: It selects stocks to buy based on the list provided in the "electricity-or-utility-stocks-to-buy-list.txt" file.

3. Cash Availability: The function checks the available cash balance and ensures there's enough cash to purchase stocks.

4. Buy Criteria: It considers specific criteria before buying stocks, such as comparing the current price to a predefined buy price and ensuring the price is within an acceptable range.

5. Error Handling: The function handles errors gracefully and logs information about each purchase, including the symbol, quantity, and purchase price.

6. Database Update: After buying stocks, the function updates the database with trade history and position information, ensuring accurate tracking of stock purchases.

7. Refresh: It triggers a refresh of the list of stocks to buy and the list of bought stocks to stay up to date with market changes.

sell_stocks Function:

1. Parallel Execution: Similar to the "buy_stocks" function, the "sell_stocks" function runs in parallel, continuously monitoring and selling stocks.

2. Stock Selection: It selects stocks to sell from the list of stocks previously bought and stored in the "bought_stocks" dictionary.

3. Sell Criteria: The function considers specific criteria before selling stocks, such as comparing the current price to a predefined sell price for profit and ensuring that stocks have been held for at least one day.

4. Error Handling: Like the "buy_stocks" function, this function handles errors gracefully and logs information about each sale, including the symbol, quantity, and sale price.

5. Database Update: After selling stocks, the function updates the database with trade history and removes the sold stocks from the list of bought stocks.

6. Refresh: It triggers a refresh of the list of bought stocks to stay up to date with any changes in the portfolio.

7. Profitable Trading: The function aims to sell stocks at a profit, enhancing the overall profitability of the trading strategy.

   These functions work together to automate the process of buying and selling stocks, making data-driven decisions based on predefined criteria, and ensuring accurate record-keeping in the database. This automation allows for efficient and timely trading in the stock market.

------------------------------------------------------------
            Performance Stock List Writer 
------------------------------------------------------------

Are you ready to make smarter investment decisions in the electricity stocks market? 
Look no further! Our Python script, the "Performance Stock List Writer," is here to help you.

------------------------------------------------------------

Key Features:
- Automated Stock Analysis: Our script automatically analyzes electricity stocks to provide you with a list of top-performing stocks.

- Regular Updates: The stock list is updated Monday thru Friday, every 24 hours,
  and every 5 minutes during most of the day when the Stock Market is open for trading to ensure you have the most current information.
  This has been really effective for keeping the most successful stocks at the top of the list of stocks to purchase. 

- Time-Specific Execution: The script runs during specific hours, allowing you to focus on other tasks without interruption.
  

- Easy Configuration: Customize your list of stock symbols in the "list-of-stock-symbols-to-scan.txt" file.

- Data-Driven Decisions: Make investment decisions based on percentage changes in stock prices over the past 14 days.

- Error Handling: The script handles errors gracefully and restarts after 5 minutes, ensuring uninterrupted performance.

------------------------------------------------------------

Get Started Today:
1. Download the script.
2. Configure your list of stock symbols.
3. Let the script do the work, providing you with a list of top electricity stocks to consider.

Invest with confidence in the electricity market. Get the "Performance Stock List Writer" now!

------------------------------------------------------------

 Next run will be soon after the time of [Next Run Time] (Eastern Time).

 Stocks list updated successfully.

------------------------------------------------------------


***************************************************************************************************************

***** This program will only work if you have 
at least 1 stock symbol in the electricity-or-utility-stocks-to-buy-list.txt 
because of the functionality of the python code to analyze stocks to buy 
at a future time. Otherwise, you will most likely see errors in the log-file-of-buy-and-sell-signals.txt. A new database file will need to be created if you started this robot without owning any stocks. Delete the database file named trading_bot.db before restarting the stockbot if the stockbot was running without any owned stock positions. 
Stop and Start the Stock Trading Robot after you have purchased at least 1 share of stock to create a new database file. I recommend linking your Alpaca Stock Trading Account with TradingView to purchase at least 1 stock position. Deciding to manually sell stocks more quickly before tomorrow can also easily be done on TradingView or on the Alpaca website for those occassional situations where your stock selling  needs to be done today instead of tomorrow. 

***** If you purchased or sold stocks through Alpaca's website or through other services, then the following 
steps must be repeated before this Stock Trading Robot can import the changes in your stock market portfolio 
and create a new database. The following steps should also fix the errors related to 
not being able to store a year-month-day for the stock position in the database; that are caused by 
stock trading without this stock market robot making the stock trades. 
***** I have found that this stock market robot is not 100% fully initialized to 
sell stocks tomorrow until it has bought or sold at least 1 share of stock 
and the share of stock has been listed under "Trade History In This Robot's Database." 
Making stock trades without using this stock market robot will also cause an error of not selling 
your stocks tomorrow unless you perform the following steps: 

        1.) Place 8 to 28 stock symbols to buy in the file named:     electricity-or-utility-stocks-to-buy-list.txt
        2.) Stop the python3 program named:      buy-and-automatically-sell-for-a-profit-robot.py
        3.) Delete the trading_bot.db file
        4.) restart this Robot with the command:      python3 buy-and-automatically-sell-for-a-profit-robot.py

        Caution: If you buy or sell stocks without using this stock market trading robot, 
        then this stock market robot will need the steps 1 thru 4, that are shown above, repeated and you will need to wait 
        an additional 24 or more hours before the stock market robot begins to be fully initialized to sell your stocks. 
        It is usually going to be an additional 24 hour waiting time unless the stocks are not in 
        a profitable price range to be sold. 

        There is a feature to allow yesterday's stocks to be sold today 
        after the trading_bot.db database file has been deleted and is brand new. 
        You set the following variable to True instead of False. The variable is: 
                     
              POSITION_DATES_AS_YESTERDAY_OPTION = False  
              
              After changing the above variable to = True, 
              you delete the files named:
              
              trading_bot_run_counter.txt and trading_bot.db
              
              Then you can sell the stocks today that 
              were purchased yesterday after deleting and creating a new trading_bot.db file.  
              Then, after running this stock robot the first time,  
              it will update the dates of the owned positions to yesterday's date.        
************************************************************************************************************

You can modify the python script to make DEBUG = True   and this will print out your stocks with the price information. 
Printing out the stock information slows down this python program, and it is recommended to change debug back to:  
DEBUG = False

Use a python code IDE like Pycharm to edit 
this python code. 

This python code is currently programmed to 
spend less money during a stock market 
recession by buying only 1 to 4 shares of stock at a time per stock symbol. 
If you want to buy different quantities of stocks, then you can edit the 
python code. To buy 20 shares of stock, in 
the program section "def buy_stocks()", locate qty_of_one_stock = 1 and change the buy order code qty_of_one_stock to look as shown below: 

qty_of_one_stock = 20


This stock market robot works best if you purchase approximately 10 to 15 different stocks at only 1 to 4 shares per stock because the stocks are sold really soon when the price is at a profitable position to sell the stock. This Stock Trading Robot has a strategy to buy stocks today for selling tomorrow because this allows for much more stock trading activity to take place within the stock trading rules of day trading 3 maximum times in 5 business days. 

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

You will need 2 command line terminals open to fully operate the Advanced Stock Market Trading Robot
because one terminal window is the robot and the other terminal window is for 
updating the list of stocks to buy with the most successful energy or electric utility company stocks. 
To select different stocks to buy and allow up to 24 hours for the stocks list to update, edit the list of stocks 
in the file named "list-of-stock-symbols-to-scan.txt". 
To immediatly select different stock symbols to buy, then edit the list of stocks 
in the file named "electricity-or-utility-stocks-to-buy-list.txt" and also 
in the file named "list-of-stock-symbols-to-scan.txt". 

python3 buy-and-automatically-sell-for-a-profit-robot.py 

open a second command line terminal and run the following command: 

python3 performance-stock-list-writer.py

The performance-stock-list-writer.py python program will make sure that only 
successful stocks are purchased by the Advanced Stock Market Trading Robot. 



Disclaimer:

This software is not affiliated with or endorsed by TradingView or Alpaca Securities, LLC. 
It aims to be a valuable tool for stock market trading, but all trading involves risks. 
Use it responsibly and consider seeking advice from financial professionals.

Ready to elevate your trading game? Download the 2023 Edition of the Advanced Stock Market Trading Robot, Version 2, and get started today!

Important: Don't forget to regularly update your list of stocks to buy and keep an eye on the market conditions. Happy trading!

Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
