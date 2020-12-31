#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) 2020 DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script installs all requirements needed for an 1.8 inch ST7735 LCD to 
# work with a raspberry pi hosting a Nextcloud server.
#-------------------------------------------------------------------------------

echo " "
echo "Downloading some things required for the library to work..."
echo " "
sudo apt update
sudo apt install build-essential python3-dev python3-smbus python3-pip python3-pil python3-numpy git

echo " "
echo "Installing the Raspberry Pi GPIO and Adafruit GPIO libraries for Python..."
echo " "
sudo python3 -m pip install RPi.GPIO
sudo python3 -m pip install Adafruit_GPIO
sudo python3 -m pip install psutil
sudo python3 -m pip install --upgrade certifi

echo " "
echo "Cloning the repository and installing the LCD library..."
echo " "
git clone https://github.com/doidotech/Python_ST7735.git
cd Python_ST7735
sudo python3 setup.py install

echo " "
echo "Changing /boot/config.txt file to allow use of SPI port..."
echo " "

echo " "
echo "Enabling SPI port..."
echo " "
sudo sed -i 's/dtparam=spi=off/dtparam=spi=on/g' /boot/config.txt
sudo sed -i 's/#dtparam=spi=on/dtparam=spi=on/g' /boot/config.txt

echo " "
echo "Done installing ST7735 LCD library."
echo " "

