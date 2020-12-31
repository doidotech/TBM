#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.2
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script is used to create a Mynode lcd service that starts at boot
# systemd is used.
#-------------------------------------------------------------------------------

# Get current working directory
cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=Mynode LCD Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 $cwd/MyNodeLCD.py
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/myNodeST7735LCD.service

# The permission on the unit file needs to be set to 644
sudo chmod 644 /lib/systemd/system/myNodeST7735LCD.service

# Configure systemd
sudo systemctl daemon-reload
sudo systemctl enable myNodeST7735LCD.service

# Start the service
sudo systemctl start myNodeST7735LCD.service
echo "Done Creating Mynode ST7735 LCD Service."

