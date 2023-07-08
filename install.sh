#!/bin/bash

echo "Starting setup..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Attempting to install..."
    sudo apt update
    sudo apt install -y python3-all
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Attempting to install..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install the necessary python packages
sudo pip3 install alpaca-trade-api yfinance pandas backtrader pytz

# Check if build-essential is installed
if ! command -v gcc &> /dev/null
then
    echo "gcc could not be found. Attempting to install build-essential..."
    sudo apt update
    sudo apt install -y build-essential
fi

# Install TA-Lib
echo "Installing TA-Lib..."
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# Check if TA-Lib installed correctly
if ! ldconfig -p | grep libta_lib.so &> /dev/null
then
    echo "TA-Lib could not be found. The installation failed..."
    exit 1
fi

# Install TA-Lib python wrapper
sudo pip3 install ta-lib

echo "Setup completed successfully."
