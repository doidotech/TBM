#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) 2020 DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.1
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script is used to create a RaspiBlitz ST7735 lcd service that starts at boot
# systemd is used.
#-------------------------------------------------------------------------------

# allow the get_btc_sync.sh file to be executable
sudo chmod +x get_btc_sync.sh

# Get current working directory
cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=RaspiBlitz ST7735 LCD Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 $cwd/RaspiblitzLCDV.py
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/raspiBlitzST7735LCD.service

# The permission on the unit file needs to be set to 644
sudo chmod 644 /lib/systemd/system/raspiBlitzST7735LCD.service

# Configure systemd
sudo systemctl daemon-reload
sudo systemctl enable raspiBlitzST7735LCD.service

# Start the service
systemctl start raspiBlitzST7735LCD.service
echo "Done Creating RaspiBlitz ST7735 LCD Service."

