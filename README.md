# The Bitcoin Machine
Repository contains LCD setup scripts for your Bitcoin Nodes

[![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/Main.jpg)](https://thebitcoinmachines.com)
# How to setup The Bitcoin Machine's LCD

The Bitcoin Machine is the first ever Bitcoin node device to have a LCD Bitcoin Ticker.
We all have a habit of checking Bitcoin Price now and then. There are some who monitors the generated bitcoin blocks and total mined Bitcoins till date. The Machine's Dashboard doesn't stop or restrict you to think beyond. It allows users to customize what to display on the LCD.

## Setup the Machine Face (LCD)
SSH into the bitcoin node using Putty or iTerm2

![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/1.png)

Clone the TBM repository
```sh
git clone https://github.com/doidotech/TBM.git
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/2.png)

```sh
cd TBM/TBMLCD-v0.1
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/3.png)

```sh
sudo chmod +x lcdSetupScript.sh
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/4.png)

```sh
sudo ./lcdSetupScript.sh
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/5.png)
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/6.png)

```sh
cd ..
sudo cp -r TBMLCD-v0.1 /usr/bin
cd /usr/bin/TBMLCD-v0.1
sudo chmod +x TBMLCDServiceSetup.sh
sudo ./TBMLCDServiceSetup.sh
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/7.png)

##### check the status of the LCD service

```sh
sudo systemctl status TBMST7735LCD.service
```
![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/8.png)

By now the LCD is UP and Running with Bitcoin Dashboard.

![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/9.jpg)

### Development

Want to contribute? Great!

### Connect with us

| Telegram | [https://t.me/TheBitcoinMachines][TBMTEL] |
| Email | support@doido.in |


 [TBMTEL]: <https://t.me/TheBitcoinMachines>
