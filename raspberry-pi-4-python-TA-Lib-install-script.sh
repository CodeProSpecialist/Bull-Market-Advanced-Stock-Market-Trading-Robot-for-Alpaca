#!/bin/bash

echo "Starting setup..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Attempting to install..."
    sudo apt update
    sudo apt install -y python3
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Attempting to install..."
    sudo apt update
    sudo apt install -y python3-pip
fi

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

./configure --build=aarch64-unknown-linux-gnu
sudo make all
sudo make install

# Check if TA-Lib installed correctly
if ! ldconfig -p | grep libta_lib.so &> /dev/null
then
    echo "TA-Lib could not be found. The installation failed..."
    exit 1
fi

# Install TA-Lib python wrapper
pip3 install TA-Lib

echo "Setup completed successfully."
