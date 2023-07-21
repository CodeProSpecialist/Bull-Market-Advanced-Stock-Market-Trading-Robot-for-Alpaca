echo "Uninstalling the extra software libraries that were installed."

pip3 uninstall alpaca-trade-api 
pip3 uninstall yfinance
pip3 uninstall pytz
pip3 uninstall pandas
pip3 uninstall tradingview_ta

sudo pip3 uninstall TA-Lib

echo "Uninstall completed successfully."
