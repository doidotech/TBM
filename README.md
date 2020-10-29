# TBM_Node
Repository contains LCD setup scripts for nodes


git clone https://github.com/doidotech/TBM_Node.git

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
