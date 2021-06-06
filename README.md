
[![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/Main.jpg)](https://thebitcoinmachines.com)
# How to setup The Bitcoin Machine's LCD

The Bitcoin Machine is the first ever Bitcoin node device to have a LCD Bitcoin Ticker.
We all have a habit of checking Bitcoin Price now and then. There are some who monitors the generated bitcoin blocks and sum of total bitcoins generated till date. we got you covered. The Machine's Dashboard doesn't stop or restrict you to think beyond. It allows users to customize what to display on the LCD.

## Setup the Machine Face (LCD)
ssh into the bitcoin node using Putty or iTerm2


Clone the TBM repository
```sh
git clone https://github.com/doidotech/TBM.git
```


```sh
cd TBM/TBMLCD-v0.4
```


```sh
sudo chmod +x lcdServiceSelector.sh
```


```sh
sudo ./lcdServiceSelector.sh
```
Enter a number to select the Node for which you are installing LCD Drivers.

Once setup complete, please reboot the machine from your node dashboard.

By now the LCD is UP and Running with Bitcoin Dashboard.

![N|Solid](https://github.com/doidotech/TBM/raw/master/Images/8.png)

### Development

Want to contribute? Great!

### Connect with us

| Telegram | [https://t.me/TheBitcoinMachines][TBMTEL] |
| Email | support@doido.in |


 [TBMTEL]: <https://t.me/TheBitcoinMachines>
