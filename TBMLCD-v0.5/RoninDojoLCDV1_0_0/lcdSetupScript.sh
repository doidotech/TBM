#!/bin/bash
#-------------------------------------------------------------------------------
#   DOIDO Technologies.
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script installs all requirements needed for an 1.8 inch ST7735 LCD to 
# work with a raspberry pi
#-------------------------------------------------------------------------------

echo " "
echo "Downloading packages required for the LCD..."
echo " "
pacman -Sy
pacman -S gcc
pacman -S base-devel git
echo " "
echo "Installing the Raspberry Pi GPIO and Adafruit GPIO libraries for Python..."
echo " "
python3 -m pip install python-dev-tools
python3 -m pip install smbus
python3 -m pip install spidev Pillow numpy
export CFLAGS=-fcommon
python3 -m pip install RPi.GPIO
python3 -m pip install Adafruit_GPIO
python3 -m pip install psutil
python3 -m pip install --upgrade certifi

echo " "
echo "Cloning the repository and installing the LCD library..."
echo " "
git clone https://github.com/doidotech/Python_ST7735.git
cd Python_ST7735
python3 setup.py install

echo " "
echo "Changing /boot/config.txt file to allow use of SPI port..."
echo " "

echo " "
echo "Enabling SPI port..."
echo " "
sed -i -e '$adtparam=spi=on' /boot/config.txt
echo " "
echo "Setup complete!"
echo " "

