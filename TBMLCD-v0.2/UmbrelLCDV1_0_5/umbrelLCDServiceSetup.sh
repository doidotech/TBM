#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script is used to create an Umbrel lcd service that starts at boot
# systemd is used.
#-------------------------------------------------------------------------------

# Get current working directory
cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=Umbrel LCD Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 $cwd/UmbrelLCD.py
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/UmbrelST7735LCD.service

# The permission on the unit file needs to be set to 644
sudo chmod 644 /lib/systemd/system/UmbrelST7735LCD.service

# Configure systemd
sudo systemctl daemon-reload
sudo systemctl enable UmbrelST7735LCD.service

# Start the service
sudo systemctl start UmbrelST7735LCD.service
echo "Done Creating Umbrel ST7735 LCD Service."

