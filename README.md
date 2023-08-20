***** Please download the newest version of this python program. 
The program code had some bugs removed. Some errors were fixed. 
This python program has been updated on August 20, 2023. *****


     This Python Stock Market Trading Bot has completely brand new, redesigned python 3 code. 
Proceed with caution because this python code is currently in beta testing mode. 

I needed to stop using the strict and somewhat buggy python Pandas Library to add more flexibility to the data frames. 
So, I am using talib and not using Pandas at all. 

***** This program will only work if you have 
at least 1 stock symbol in the electricity-or-utility-stocks-to-buy-list.txt 
because of the functionality of the python code to analyze stocks to buy 
at a future time. Otherwise, you will most likely see errors in the log-file-of-buy-and-sell-signals.txt. *****

You can modify the python script to make DEBUG = True   and this will print out your stocks with the price information. 
Printing out the stock information slows down this python program, and it is recommended to change debug back to:  
DEBUG = False

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


   I also recommend to not select stocks that are valued less than 200 dollars to have the stocks work well 
with this stock bot because it is more worth your time to use your single or last few day trades 
to generate a larger dollar amount of profit from a 2 percent profit before the stock is sold. 
I also recommend only having this stock bot monitor your favorite stock that you have 
noticed increasing in price numbers. This will make this stock bot generate the most profit for 
you in the least amount of time. 

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
