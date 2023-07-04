# Stock-Market-Robot-Version-2

This code is so brand new that it is still being written and developed, so it is still in the beta testing phase right now. 
It still might work, though. 

Stock Market Robot This is a stock market portfolio management application that helps minimize losses and maximize profits.
This works with the Alpaca stock market trading broker. 
Stock Market Robot only works Monday through Friday: 9:30am - 4:00pm Eastern Time.

This is an Advanced buying and selling robot to monitor a stock market symbol that you type in. 

It will automatically buy more stock of the symbol that you have selected when there is a bull market 
or a price increase and it will automatically sell all shares of the same symbol when there is a bear market 
or a price decrease. 


To install:

Do not be the root user. This installs from a regular user account. Open a command line terminal from this folder location and type: sh install.sh

Remember that you just let the stockbot run for 24 hours. It watches the prices of the stocks that you own in your alpaca account. It sells the stocks to prevent losing money. The python code named: sell-when-price-increases-or-decreases-stockbot.py will sell your stocks both during a price decrease and during a price increase to help you to not miss out on obtaining those rare profit opportunities that quickly take place in the stock market. If these fast price increases are not noticed quickly, then they are usually missed and then the price usually decreases afterwords.

After placing your alpaca keys at the bottom of /home/nameofyourhomefolderhere/.bashrc you simply run the command in a command terminal like:

python3 stock-market-buying-selling-robot-v2.py




Disclaimer: Remember that all trading involves risks. The ability to successfully implement these strategies depends on both market conditions and individual skills and knowledge. As such, trading should only be done with funds that you can afford to lose. Always do thorough research before making investment decisions, and consider consulting with a financial advisor. This is use at your own risk software. This software does not include any warranty or guarantees other than the useful tasks that may or may not work as intended for the software application end user. The software developer shall not be held liable for any financial losses or damages that occur as a result of using this software for any reason to the fullest extent of the law. Using this software is your agreement to these terms. This software is designed to be helpful and useful to the end user.

Place your alpaca code keys in the location: /home/name-of-your-home-folder/.bashrc Be careful to not delete the entire .bashrc file. Just add the 4 lines to the bottom of the .bashrc text file in your home folder, then save the file. .bashrc is a hidden folder because it has the dot ( . ) in front of the name. Remember that the " # " pound character will make that line unavailable. To be helpful, I will comment out the real money account for someone to begin with an account that does not risk using real money. The URL with the word "paper" does not use real money. The other URL uses real money. Making changes here requires you to reboot your computer or logout and login to apply the changes.

The 4 lines to add to the bottom of .bashrc are:

export APCA_API_KEY_ID='zxzxzxzxzxzxzxzxzxzxz'

export APCA_API_SECRET_KEY='zxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzxzx'

#export APCA_API_BASE_URL='https://api.alpaca.markets'

export APCA_API_BASE_URL='https://paper-api.alpaca.markets'
