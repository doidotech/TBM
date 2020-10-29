# The Bitcoin Machine
Repository contains LCD setup scripts for your Bitcoin Nodes

To Setup Bitcoin Ticker on your Bitcoin Machine LCD, SSH into your Bitcoin Node and follow the steps below,


git clone https://github.com/doidotech/TBM.git

cd TBM/TBMLCD-v0.1

sudo chmod +x lcdSetupScript.sh

sudo ./lcdSetupScript.sh

cd ..

sudo cp -r TBMLCD-v0.1 /usr/bin

cd /usr/bin/TBMLCD-v0.1

sudo chmod +x TBMLCDServiceSetup.sh

sudo ./TBMLCDServiceSetup.sh

sudo systemctl status TBMST7735LCD.service

************************************************
