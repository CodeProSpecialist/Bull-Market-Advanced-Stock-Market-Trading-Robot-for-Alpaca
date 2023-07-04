#!/bin/bash

# Update package lists
sudo apt-get update

# Install Python3 pip
sudo apt-get install python3-pip



# Install necessary Python packages
pip3 install alpaca-trade-api 
pip3 install yfinance
pip3 install pytz
