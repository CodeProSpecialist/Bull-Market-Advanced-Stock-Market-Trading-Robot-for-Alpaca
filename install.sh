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
sudo pip3 install alpaca-trade-api yfinance pytz pandas import pandas_ta numpy

# Check if build-essential is installed
if ! command -v gcc &> /dev/null
then
    echo "gcc could not be found. Attempting to install build-essential..."
    sudo apt update
    sudo apt install -y build-essential
fi



echo "Setup completed successfully."
