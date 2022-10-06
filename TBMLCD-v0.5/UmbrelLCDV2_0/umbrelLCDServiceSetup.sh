#!/bin/bash
#-------------------------------------------------------------------------------
#   Copyright (c) DOIDO Technologies
#   Version  : 1.0.3
#   Location : github
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# This script is used to create Umbrel lcd service.
# It also enables the user to select screens and currency to be used.
#-------------------------------------------------------------------------------

# Screen selection menu
echo "=================================================================================="
echo "                              SCREEN SELECTION MENU"
echo "=================================================================================="
echo
echo "Available screens to be displayed on the LCD:"
echo "                    Screen 1: Bitcoin price and sats/unit of currency."
echo "                    Screen 2: Next Bitcoin block information."
echo "                    Screen 3: Current Bitcoin block height."
echo "                    Screen 4: Current date and time."
echo "                    Screen 5: Bitcoin network information."
echo "                    Screen 6: Payment channels information."
echo "                    Screen 7: Disk storage information."
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
    	read -p "Would you like screen 1 to be displayed on the LCD?  " userAnswer
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
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 2
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 2 to be displayed on the LCD?  " userAnswer
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
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 3
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 3 to be displayed on the LCD?  " userAnswer
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
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 4
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 4 to be displayed on the LCD?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 4. \e[0m"
                userScreenChoices="${userScreenChoices}Screen4,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 4."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 5
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 5 to be displayed on the LCD?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 5. \e[0m"
                userScreenChoices="${userScreenChoices}Screen5,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 5."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 6
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 6 to be displayed on the LCD?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 6. \e[0m"
                userScreenChoices="${userScreenChoices}Screen6,"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 6."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
		fi
	done

# Get user choice about screen 7
gettingUserChoice=true
# Loop until user enters a valid choice
while $gettingUserChoice 
	do
    	read -p "Would you like screen 7 to be displayed on the LCD?  " userAnswer
        # Convert to uppercase
		userAnswer=${userAnswer^^}

		# Check if entered a valid option
		if [ $userAnswer == "YES" ]
            then
                echo -e "\e[1;32m Adding screen 7. \e[0m"
                userScreenChoices="${userScreenChoices}Screen7"
                gettingUserChoice=false
		elif [ $userAnswer == "NO" ]
            then
                echo "Not Adding screen 7."
                gettingUserChoice=false
		else
           echo -e "\e[1;31m Your answer is not valid. \e[0m"
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
    			echo "Creating Umbrel ST7735 LCD Service."
    			gettingCurrency=false
			
				# Get current working directory
				cwd=$(pwd)

# Create A Unit File
sudo echo "[Unit]
Description=Umbrel LCD Service
After=multi-user.target
[Service]
Restart=on-failure
RestartSec=30s
Type=idle
ExecStart=/usr/bin/python3 $cwd/UmbrelLCD.py $newCurrency $userScreenChoices
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
		else
    			#echo "Entered Currency code is not valid!!!"
    			echo -e "\e[1;31m Entered Currency code is not valid!!! \e[0m"
		fi
	done
