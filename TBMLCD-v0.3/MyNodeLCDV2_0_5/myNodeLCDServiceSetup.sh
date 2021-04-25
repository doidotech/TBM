#!/bin/bash
#-------------------------------------------------------------------------------
# This script is used to create an Mynode lcd service that starts at boot
#-------------------------------------------------------------------------------

# Get user currency
gettingCurrency=true

# Loop until user enters a valid currency
while $gettingCurrency 
	do
    	echo
		read -p "Please Enter Currency Code e.g. USD for US Dollar: " newCurrency
		# Convert to uppercase
		newCurrency=${newCurrency^^}
		echo $newCurrency

		# Check if user entered a valid currency code
		validationResult=$(python3 ./CurrencyData.py ${newCurrency})
		if [ "$validationResult" = "Valid" ]; then
    			echo "Enabling MynodeLCD to run on boot..."
    			gettingCurrency=false
			
				# Get current working directory
				cwd=$(pwd)

# Enabling LCD to run on Boot
echo " "
echo " "
sudo sed -i '/sudo python3/s/^/#/g' /etc/rc.local
sudo sed -i "/fi/a sudo python3 /home/admin/TBM/TBMLCD-v0.3/MyNodeLCDV2_0_5/MyNodeLCD.py $newCurrency &" /etc/rc.local
		else
    			#echo "Entered Currency code is not valid!!!"
    			echo -e "\e[1;31m Entered Currency code is not valid!!! \e[0m"
		fi
	done


	
	