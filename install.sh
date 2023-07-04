#!/bin/bash

# Update package lists
sudo apt-get update

# Install Python3 pip
sudo apt-get install python3-pip

# Install TA-Lib dependencies
sudo apt-get install libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev gfortran pkg-config

# Download TA-Lib, unpack it, compile it, and install it
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar xvzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# Install necessary Python packages
pip3 install alpaca-trade-api pandas pytz yfinance ta-lib
