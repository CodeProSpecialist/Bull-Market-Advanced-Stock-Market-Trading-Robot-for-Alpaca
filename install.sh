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

# Create and activate virtual environment in the user's home directory
HOME_VENV_PATH="$HOME/My-Python-Virtual-Environment-Packages"
VENV_PATH="$HOME_VENV_PATH/venv"

# Check if the virtual environment directory exists, if not, create it
if [ ! -d "$VENV_PATH" ]; then
    mkdir -p "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install Python packages within the virtual environment
pip3 install yfinance alpaca-trade-api sqlalchemy pytz ta-lib schedule

# Install TA-Lib dependencies  
echo "Installing TA-Lib dependencies ..."
sudo apt-get install libatlas-base-dev gfortran -y

# Download and install TA-Lib
echo "Downloading TA-Lib..."
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
echo "Configuring TA-Lib..."
./configure --prefix=/usr
echo "Installing TA-Lib..."
make
sudo make install

cd ..
rm -r ta-lib
rm ta-lib-0.4.0-src.tar.gz

# Deactivate the virtual environment
deactivate

echo "All done! You can now run your Python script."
