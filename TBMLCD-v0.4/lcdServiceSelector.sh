#!/bin/bash
#-------------------------------------------------------------------------------
#   DOIDO Technologies
#   File : lcdServiceSelector.sh
#   Version  : 1.0.3
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script allows the user to select and install LCD Drivers among the following Nodes:
#		1. Umbrel
#		2. Raspiblitz
#		3. MyNode
#		4. RoninDojo
#-------------------------------------------------------------------------------

# Define a function to ask user to reboot the device
reboot_device(){
echo
echo "A reboot is necessary to complete the LCD setup."
echo "Please reboot the machine from your Node dashboard."
}

# Define a function to check if a service is active before uninstalling it
uninstall_services(){
# Check if one of the services is already installed
echo
echo "Checking if one of the following services is installed:"
echo
echo "			1. Umbrel"
echo "			2. Raspiblitz"
echo "			3. MyNode"
echo "			4. RoninDojo"
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

# Check RoninDojo service
STATUS="$(systemctl is-active RoninDojoST7735LCD.service)"
if [ "${STATUS}" = "active" ]; then
    echo "Uninstalling RoninDojoST7735LCD.service"
    sudo systemctl stop RoninDojoST7735LCD.service
    sudo systemctl disable RoninDojoST7735LCD.service
    sudo rm /lib/systemd/system/RoninDojoST7735LCD.service
    sudo systemctl daemon-reload
else 
    echo "RoninDojoST7735LCD.service not running."   
fi

}

# Uninstall any existing services
uninstall_services

# Get user choice
gettingUserChoice=true

# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	echo
    	echo "Please enter a number to select the Node for which you are installing LCD Drivers:"
    	echo
    	echo "			1 For Umbrel"
    	echo "			2 For Raspiblitz"
    	echo "			3 For MyNode"
		echo "			4 For RoninDojo"
    	echo "			0 To Exit"
    	echo
		read -p "LCD service: " newLCDService
		echo
		echo

		# Check if entered a valid option
		if [ $newLCDService == 1 ]
		then
		   echo "Creating Umbrel LCD service."
		   gettingUserChoice=false
		   # Install lcd driver
		   cd UmbrelLCDV1_0_10
		   sudo chmod +x lcdSetupScript.sh
		   sudo ./lcdSetupScript.sh
		   # Install lcd service
		   cd ..
		   sudo cp -r UmbrelLCDV1_0_10 /usr/bin
		   cd /usr/bin/UmbrelLCDV1_0_10
		   sudo chmod +x umbrelLCDServiceSetup.sh
		   sudo ./umbrelLCDServiceSetup.sh
		   # Ask user to Reboot
		   reboot_device
		elif [ $newLCDService == 2 ]
		then
		   echo "Creating Raspiblitz LCD service."
		   gettingUserChoice=false
		   # Install lcd driver
		   cd RaspiBlitzLCDV1_0_7
		   sudo chmod +x lcdSetupScript.sh
		   sudo ./lcdSetupScript.sh
		   # Install lcd service
		   cd ..
		   sudo cp -r RaspiBlitzLCDV1_0_7 /usr/bin
		   cd /usr/bin/RaspiBlitzLCDV1_0_7
		   sudo chmod +x raspiBlitzLCDServiceSetup.sh
		   sudo ./raspiBlitzLCDServiceSetup.sh
		   # Ask user to Reboot
		   reboot_device
		elif [ $newLCDService == 3 ]
		then
		   echo "Creating MyNode LCD service."
		   gettingUserChoice=false
		   # Install lcd driver
		   cd MyNodeLCDV2_0_6
		   sudo chmod +x lcdSetupScript.sh
		   sudo ./lcdSetupScript.sh
		   # Install lcd service
		   cd ..
		   sudo cp -r MyNodeLCDV2_0_6 /usr/bin
		   cd /usr/bin/MyNodeLCDV2_0_6
		   sudo chmod +x myNodeLCDServiceSetup.sh
		   sudo ./myNodeLCDServiceSetup.sh
		   # Ask user to Reboot
		   reboot_device
		   elif [ $newLCDService == 4 ]
		then
		   echo "Creating RoninDojo LCD service."
		   gettingUserChoice=false
		   # Install lcd driver
		   cd RoninDojoLCDV1_0_0
		   sudo chmod +x lcdSetupScript.sh
		   sudo ./lcdSetupScript.sh
		   # Install lcd service
		   cd ..
		   sudo cp -r RoninDojoLCDV1_0_0 /usr/bin
		   cd /usr/bin/RoninDojoLCDV1_0_0
		   sudo chmod +x RoninDojoLCDServiceSetup.sh
		   sudo ./RoninDojoLCDServiceSetup.sh
		   # Ask user to Reboot
		   reboot_device
		elif [ $newLCDService == 0 ]
		then
		   echo "Exiting service selection"
		   gettingUserChoice=false
		else
		   echo "Please enter a valid option"
		fi
	done

