#!/bin/bash
#-------------------------------------------------------------------------------
# This script is used to create lcd service that starts at boot.
# It also enables the user to select screens and currency to be used.
#-------------------------------------------------------------------------------

# Display the screen selection menu
echo "=============================================================================================="
echo "                                    SCREEN SELECTION MENU"
echo "=============================================================================================="
echo
echo "Available screens:"
echo "                    Screen 1: Bitcoin Price and sats/currency."
echo "                    Screen 2: Mempool information."
echo "                    Screen 3: Current Bitcoin Block height."
echo "                    Screen 4: Current Date and Time."
echo
echo "Please answer by typing yes or no then press the enter key."
echo

# a string to hold user screen choices
userScreenChoices=""
# Get user choice about screen 1
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like Bitcoin price and sats/currency to be shown as screen1?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 1. \e[0m"
                userScreenChoices="${userScreenChoices}Screen1,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 1."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer was not valid. \e[0m"
		fi
	done

# Get user choice about screen 2
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like Mempool information to be shown as screen 2?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 2. \e[0m"
                userScreenChoices="${userScreenChoices}Screen2,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 2."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer was not valid. \e[0m"
		fi
	done

# Get user choice about screen 3
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like Current Bitcoin Block height to be shown as screen 3?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 3. \e[0m"
                userScreenChoices="${userScreenChoices}Screen3,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 3."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer was not valid. \e[0m"
		fi
	done

# Get user choice about screen 4
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like Current Date and Time to be shown as screen 4?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 4. \e[0m"
                userScreenChoices="${userScreenChoices}Screen4"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 4."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer was not valid. \e[0m"
		fi
	done

echo "User choices: ${userScreenChoices}"
echo

echo "=============================================================================================="
echo "                                      CURRENCY SELECTION"
echo "=============================================================================================="
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
    			echo "Creating Raspiblitz ST7735 LCD Service."
    			gettingCurrency=false
			
				# Get current working directory
				cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=Raspiblitz LCD Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 $cwd/RaspiblitzLCD.py $newCurrency $userScreenChoices
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/RaspiblitzST7735LCD.service

				# The permission on the unit file needs to be set to 644
				sudo chmod 644 /lib/systemd/system/RaspiblitzST7735LCD.service

				# Configure systemd
				sudo systemctl daemon-reload
				sudo systemctl enable RaspiblitzST7735LCD.service

				# Start the service
				sudo systemctl start RaspiblitzST7735LCD.service
				echo "Done Creating Raspiblitz ST7735 LCD Service."
		else
    			#echo "Entered Currency code is not valid!!!"
    			echo -e "\e[1;31m Entered Currency code is not valid!!! \e[0m"
		fi
	done
