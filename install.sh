#!/bin/bash

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo Python 3 is installed
else
    echo Python 3 is not installed
    sudo apt-get update
    sudo apt-get install python3-all
    sudo apt-get install python3-pip
fi

# Check if pip is installed
if command -v pip3 &>/dev/null; then
    echo pip3 is installed
else
    echo pip3 is not installed
    sudo apt install python3-pip
fi

# Now we can install our Python 3 packages
pip3 install --upgrade pip

# Install necessary Python packages
pip3 install alpaca-trade-api 
pip3 install yfinance
pip3 install pytz
