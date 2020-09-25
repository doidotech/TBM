# TBM_Node
Repository contains LCD setup scripts for nodes

--LCD SETUP for Umbrel Node --

git clone https://github.com/doidotech/TBM_Node.git

cd UmbrelLCD-v0.1

sudo chmod +x lcdSetupScript.sh
sudo ./lcdSetupScript.sh
cd ..
sudo cp -r UmbrelLCD-v0.1 /usr/bin
cd /usr/bin/UmbrelLCD-v0.1
sudo chmod +x umbrelLCDServiceSetup.sh
sudo ./umbrelLCDServiceSetup.sh
sudo systemctl status UmbrelST7735LCD.service
