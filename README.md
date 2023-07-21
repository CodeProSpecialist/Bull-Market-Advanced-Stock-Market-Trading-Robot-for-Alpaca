
***** I am in the middle of fixing a code bug 
in the Chandelier exit sell method. 
 the error should be fixed within 24 hours. 
 feel free to download a previously working 
version of this code on github. 

# Advanced-Stock-Market-Trading-Bot-Version-2 

This Advanced Stock Market Robot seems to be working great. 
Important note: This Stock Market Robot will quickly sell any stocks 
that decrease in value, even just by 1 penny to prevent losing any money 
at all during the 2023 Stock Market Recession. 

Important Instructions: 
1. Place this program into "buy more stocks mode"
    when you put stock symbols in the text file "successful-stocks-list.txt"
    and the stock market trading robot keeps looking for chances to buy more stocks
   from the list of stock symbols.

2. This program will automatically remove the stock symbol name
   from the text file "successful-stocks-list.txt" after an order to buy stock has
   been placed. This will allow you to not have to do anything while the
   Stock Market Robot is working for you. 

4. Place this program into "sell stocks only mode" by deleting all of the
   stock symbols in the text file called: "successful-stocks-list.txt. "
   This includes when you want to try to sell stocks for a profit when the price of the stock
   is increasing in value. 

   
The code block sell_dropped_stocks() is a function that checks the current positions of stocks held by the account and performs several checks before deciding whether to sell any of the stocks.

Here's a breakdown of what the code does:

    Get current positions: It retrieves the current positions from the Alpaca API using api.list_positions() and assigns them to the positions variable.

    Loop through each position: It iterates over each position in the positions list.

    Get the current price: It retrieves the current price of the stock from the Position object and assigns it to the current_price variable.

    Initialize variables: It initializes several variables related to trailing stop loss and consecutive price decreases. These variables include highest_price (the highest price the stock has reached since entry), stop_loss_percentage (the percentage below the highest price to set the stop loss price), stop_loss_price (the calculated stop loss price), stop_loss_triggered (a flag to indicate if the stop loss has been triggered), consecutive_decreases (the count of consecutive price decreases), and previous_price (the previous price for comparison).

    Check if the price meets the sell conditions: It checks two conditions to determine if the stock should be sold:
        If the current price is less than the average entry price minus 1 (dollar). This condition allows for selling if the price drops by more than 1 dollar from the average entry price.
        If there are three or more consecutive price decreases. This condition allows for selling if the price has been decreasing for three consecutive intervals.

    Sell the stock: If the sell conditions are met, it executes the sell operation. The code checks if the quantity of shares (position.qty) is greater than 0 and if the day trade count (account.daytrade_count) is less than 3 before submitting the order to sell the stock using api.submit_order() with the specified parameters.

    Update trailing stop loss and consecutive price decreases: It updates the trailing stop loss and consecutive price decrease variables based on the current price. If the current price is higher than the previous highest price, the highest_price is updated, and the stop_loss_price is recalculated based on the new highest price. If the current price is lower than the previous price, the consecutive_decreases count is incremented. If the current price is higher or the same as the previous price, the consecutive_decreases count is reset to 0.

    Check if stop loss is triggered: It compares the current price with the calculated stop loss price to check if the stop loss condition has been triggered. If the current price is lower than the stop loss price, the stop_loss_triggered flag is set to True.

    Update previous price for the next iteration: It updates the previous_price variable with the current price, so it can be used for comparison in the next iteration.

    Wait before repeating the process: It pauses the execution for 15 seconds before repeating the process, allowing for a delay between each iteration of the loop.

Overall, the code evaluates the sell conditions, executes the sell operation if the conditions are met, and tracks trailing stop loss and consecutive price decreases to make informed decisions on when to sell the stocks. 

   The Buy and Sell Functions: This python code includes buy_stock and sell_stock functions 
to perform trading actions based on the strategy. The functions consider account’s available cash 
and day trade limit, which is a good practice. Additionally, bearish conditions and 
the past 6-month performance are considered before buying a stock to avoid buying into a downtrending stock.

Never buy any stock less than 200 dollars with a stock robot 
because the stock is too unstable to work very well with a stock robot. 
More stable price increases will work the best with a stock robot 
and that would be stock that is 200 dollars or more, 
stock that is a strong buy bull stock, 
and you want to buy stock that has been increasing in price since 
the past 3 - 12 months. 

   I also recommend to not select stocks that are valued less than 200 dollars to have the stocks work well 
with this stock bot because it is more worth your time to use your single or last few day trades 
to generate a larger dollar amount of profit from a 2 percent profit before the stock is sold. 
I also recommend only having this stock bot monitor your favorite top 2 or 3 stocks that you have 
noticed increasing in price numbers. This will make this stock bot generate the most profit for 
you in the least amount of time. 

Advanced Stock Market Trading Bot

This is a stock market portfolio management application that helps minimize losses and maximize profits.
This works with the Alpaca stock market trading broker. 
Advanced Stock Market Trading Bot only works Monday through Friday: 9:30am - 4:00pm Eastern Time.

This is an Advanced buying and selling Python 3 Trading Robot 
to monitor a stock market symbol or a number of stock symbols that you place in the file "successful-stocks-list.txt". 
Only place one stock symbol on each line. 

It will automatically buy more stock of the symbol that you have selected when there is a bull market 
or a price increase and it will automatically sell all shares of the same symbol when there is a bear market or a price decrease. 
It helps to prevent from buying bearish stocks with 2 bearish stock checks 
and this feature will almost completely prevent buying the stocks that are losing price value. 
After buying or selling a stock, this Trading Robot waits for 10 minutes to resume working to wait for the 
order to finish processing. This prevents numerous orders for the same stocks from being placed. 
It stops buying more stocks if you have a Daytrade Count of 3 days to comply with the PDT or Pattern Daytrading Rules. 
It maximizes your profits by trading with all of the available Cash Equity in your stock broker account. Here's more information: 

Experience the power of Python 3's TA Library with our Advanced Stock Market Trading Bot. Turn data into insights, insights into decisions, and decisions into profit. Experience the future of trading with our Advanced Stock Market Trading Bot. 
Elevate your trading game, maximize your profits, and let our bot do the heavy lifting. This isn't just a bot, it's your 24/7 trading partner.

Imagine having a personal stock market advisor available 24/7, assessing opportunities, risks, and making decisions without ever needing a break. Welcome to the future of trading with our revolutionary Advanced Trading Bot! Our robot leverages the power of Alpaca API and the newest online stock market data to keep its finger on the pulse of the market. It continually monitors your specified stocks, utilizing the most advanced trading indicators including MACD, RSI, and Moving Averages to make the most informed buy and sell decisions.
Even better, it's not just about buying and selling. This trading bot is meticulous with your account management - keeping track of your account cash, monitoring day trade counts, and providing real-time updates on your positions: 
And the best part? You're in control. You can input the stock symbols you want to trade and edit them anytime. 
Plus, it's flexible, running in any market conditions. Whether the market is open or not, our bot is hard at work, strategizing and waiting for the right moment to buy profitable stock. In a world full of data, making sense of it all can be overwhelming. That's where our Stock Market Trading Bot and the power of Python 3's TA (Technical Analysis) Library come in. The TA Library is the master key to unlocking the potential of your trading. It is a comprehensive software suite that allows our bot to tap into a myriad of technical analysis indicators. This isn't just average data, this is high-precision, deeply-analyzed metrics that give you a cutting-edge advantage in the market. Our Advanced Stock Market Trading Bot, armed with the TA Library, processes market data in real-time, applying rigorous mathematical analysis to identify key trends and indicators. From Moving Averages, MACD, to RSI, this bot can leverage them all, providing you with clear, data-driven buy and sell signals. The TA Library isn't a perfect market prediction software tool, but it's close to being perfect.  With its predictive analytics capabilities, it enables our Robot to analyze price movements, estimate future price changes, and reduce risks, leading to more informed and profitable trading decisions.

To install:

Do not be the root user. This installs from a regular user account. 
***** The below install commands are ONLY for a Desktop or Laptop Computer x86_64 type of install. ***** 
Open a command line terminal from this folder location and type: 

sh install.sh ;
sh desktop-computer-python3-TA-Lib-install.sh

sudo pip3 install ta-lib

(do not use the Raspberry Pi 4 install script unless you are installing on a Raspbery Pi 4)

Remember that you just let the stockbot run for 24 hours. It watches the prices of the stocks that you own in your alpaca account. It sells the stocks to prevent losing money. This Python program will sell your stocks both during a price decrease and during a price increase to help you to not miss out on obtaining those rare profit opportunities that quickly take place in the stock market. If these fast price increases are not noticed quickly, then they are usually missed and then the price usually decreases afterwards.

After placing your alpaca keys at the bottom of /home/nameofyourhomefolderhere/.bashrc you simply run the command in a command terminal like:

python3 advanced-stock-market-trading-robot-v2.py



Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
