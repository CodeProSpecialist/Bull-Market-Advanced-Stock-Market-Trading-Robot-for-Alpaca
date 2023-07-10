# Advanced-Stock-Market-Trading-Bot-Version-2 

This code is so brand new that it is still considered the "beta" version for about 14 days. 
It seems to be working great so far. 
There is a known small error that is: Error: No objects to concatenate, and this error can be 
ignored because it just simply reached the end of the text file and could not find any more 
stock symbols to concatenate or evaluate. 
The program seems to be working great without any problems. 

I do not know of any other stock market robot that has been designed as well as this stock market robot 
because the design uses backtrader with talib: Moving Average Convergence Divergence, 
Relative Strength Index, and Bollinger Bands that were designed 
in the busy 1980s era of the stock market to follow normal price flexibility. 
Bollinger Bands can also help determine when it is time to sell stock when the stock reaches the 
upper band level for a profit or the lower band level to prevent loss of profit. 

This stock market robot is currently configured to buy and sell stock based on the 
Bollinger Bands, RSI, and Moving Average Convergence Divergence. 
This is the best designed stock market robot that I know of that is using 
the talib and these features. 
This means that your chances of selling at a profit are increased. 

     I recommend to not select stocks that are valued less than 37.50 to have the stocks work well 
with this stock bot because it is more worth your time to use your single or last few day trades 
to generate a larger dollar amount of profit from a 3% profit before the stock is sold. 
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
It stops buying more stocks if you have a Daytrade Count of 2 days for you to use the 3rd Daytrade 
to sell a stock that has a price that is decreasing. You may change this number in this Python code if you like, 
although it is at the best setting for preventing loss of profit by default. 
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
