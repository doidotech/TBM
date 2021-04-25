#!/bin/bash
#-------------------------------------------------------------------------------
#   DOIDO Technologies.
#   File   : Uninstall.sh
#   Version  : 1.0.0
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script allows the user to select and install LCD Drivers among the following Nodes:
#		1. Umbrel
#		2. Raspiblitz
#		3. MyNode
#-------------------------------------------------------------------------------

# Define a function to check if a service is active before uninstalling it
uninstall_services(){
# Check if one of the services is already installed
echo
echo "Checking if one of the following services are installed."
echo
echo "			1. Umbrel"
echo "			2. Raspiblitz"
echo "			3. MyNode"
echo

# Check umbrel service
STATUS="$(systemctl is-active UmbrelST7735LCD.service)"
if [ "${STATUS}" = "active" ]; then
    echo "Uninstalling UmbrelST7735LCD.service"
    sudo systemctl stop UmbrelST7735LCD.service
    sudo systemctl disable UmbrelST7735LCD.service
    sudo rm /lib/systemd/system/UmbrelST7735LCD.service
    sudo systemctl daemon-reload
else 
    echo "UmbrelST7735LCD.service not running."   
fi

# Check Raspiblitz service
STATUS="$(systemctl is-active raspiBlitzST7735LCD.service)"
if [ "${STATUS}" = "active" ]; then
    echo "Uninstalling raspiBlitzST7735LCD.service"
    sudo systemctl stop raspiBlitzST7735LCD.service
    sudo systemctl disable raspiBlitzST7735LCD.service
    sudo rm /lib/systemd/system/raspiBlitzST7735LCD.service
    sudo systemctl daemon-reload
else 
    echo "raspiBlitzST7735LCD.service not running."   
fi

# Check MyNode service
STATUS="$(systemctl is-active myNodeST7735LCD.service)"
if [ "${STATUS}" = "active" ]; then
    echo "Uninstalling myNodeST7735LCD.service"
    sudo systemctl stop myNodeST7735LCD.service
    sudo systemctl disable myNodeST7735LCD.service
    sudo rm /lib/systemd/system/myNodeST7735LCD.service
    sudo systemctl daemon-reload
else 
    echo "myNodeST7735LCD.service not running."   
fi

}

# Uninstall any existing services
uninstall_services

