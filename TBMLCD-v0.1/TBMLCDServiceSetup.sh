#!/bin/bash
#-------------------------------------------------------------------------------
#   Author   : Walter-DOIDO Technologies
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script is used to create an TBM lcd service that starts at boot
# systemd is used.
#-------------------------------------------------------------------------------

# Get current working directory
cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=TBM LCD Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 $cwd/TBMLCD.py
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/TBMST7735LCD.service

# The permission on the unit file needs to be set to 644
sudo chmod 644 /lib/systemd/system/TBMST7735LCD.service

# Configure systemd
sudo systemctl daemon-reload
sudo systemctl enable TBMST7735LCD.service

# Start the service
sudo systemctl start TBMST7735LCD.service
echo "Done Creating TBM ST7735 LCD Service."

