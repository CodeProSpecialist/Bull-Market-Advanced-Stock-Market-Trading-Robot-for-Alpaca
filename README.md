

   In the ever-changing world of the stock market, opportunity can rise and fall in an instant...

That's why we've developed the ultimate tool to help you seize the moment and maximize your profits. 

Meet your new ally, the state-of-the-art, Advanced Stock Market Day Trading Robot. 

Harnessing the power of cutting-edge Python 3 programming code and sophisticated financial algorithms, 

our Day Trading Robot is designed to operate with precision and speed that's beyond human capabilities. 

It leverages the renowned MACD Indicator for reliable buy and sell signals. 

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

Defining functions: The script defines several important functions:

    load_stocks_list(): This function reads the list of stocks from the file successful-stocks-list.txt.

    get_data(symbol): This function downloads the stock price data for a given symbol. 

    remove_symbol(symbol, filename1): This function removes a given symbol from the list of stocks in the file successful-stocks-list.txt.

    MACD_Strategy(df, risk): This function implements the MACD strategy. It calculates the MACD and signal line for the given dataframe of stock prices, and generates buy and sell signals based on these values.

    MACD_color(df): This function generates a list of boolean values based on whether the MACD histogram value of the current period is greater than the previous period.

    make_order(api, symbol, qty, side): This function submits a market order to the Alpaca API.

        check_cash(api, symbol): This function checks the amount of cash available in the trading account and calculates the maximum quantity of a stock that can be bought with that cash.

    get_position_qty(api, symbol): This function retrieves the quantity of a particular stock currently held in the trading account.

    plot_macd_graph(data, symbol): This function plots a graph of the stock price and the MACD indicators. It shows the stock's closing price, the MACD line, the signal line, and the MACD histogram. It also marks the points where the MACD strategy generated buy and sell signals.

    stop_if_stock_market_is_closed(): This function checks if the current time is within the stock market's operating hours (9:30 am - 4:00 pm Eastern Time, Monday to Friday). If the market is closed, the function waits until it opens.

    main(): This is the main function that runs the trading bot. It first checks if the stock market is open. Then it enters a loop where it checks the current positions in the trading account and the list of stocks to buy. For each stock in the list, it downloads the stock price data, calculates the MACD indicators, and generates buy and sell signals. If a buy signal is generated and the account has not exceeded the day trading limit, it places a buy order. If a sell signal is generated, it places a sell order. After each buy order, it waits for 7 minutes to allow the account to update before placing more orders.

The if __name__ == "__main__": block at the end is the entry point of the script. When the script is run directly (not imported as a module), it calls the main() function. If the script is interrupted by the user (with Ctrl+C, for example), it prints a message and exits. If any other exception occurs, it prints the error message and restarts the main() function after a 2-second delay.

Please note that this script is designed to run during the stock market's operating hours. 

This Advanced Stock Market Robot seems to be working great. 
Important note: This Stock Market Robot will quickly sell any stocks 
that decrease in value, sometimes even selling just by 1 penny to prevent losing any money 
at all during the 2023 Stock Market Recession. 

This Stock Market Robot will work best to quickly sell stocks that are decreasing in price value 
by reacting to a Moving Average Convergence / Divergence "Sell Signal." 
It also reacts to quickly buy new stocks by reacting to an extremely accurate 
Moving Average Convergence / Divergence "Buy Signal." 

Important Instructions: 
     To buy and sell stocks, run the python script named buy-and-automatically-sell-for-a-profit-robot.py 
with the command: python3 buy-and-automatically-sell-for-a-profit-robot.py 
 Place this program into "buy more stocks mode" 
 when you put stock symbols in the text file "successful-stocks-list.txt"
 and the stock market trading robot keeps looking for chances to buy more stocks
 from the list of stock symbols.

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
I also recommend only having this stock bot monitor your favorite stock that you have 
noticed increasing in price numbers. This will make this stock bot generate the most profit for 
you in the least amount of time. 

Advanced Stock Market Trading Bot

This is a stock market portfolio management application that helps minimize losses and maximize profits.
This works with the Alpaca stock market trading broker. 
Advanced Stock Market Trading Bot only works Monday through Friday: 9:30am - 4:00pm Eastern Time.

This is an Advanced buying and selling Python 3 Trading Robot 
to monitor a stock market symbol or a number of stock symbols that you place in the file "successful-stocks-list.txt". 
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
