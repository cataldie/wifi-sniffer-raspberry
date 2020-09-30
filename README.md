# wifi-sniffer-raspberry
#install MySQL
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install mariadb-server
$ sudo mysql_secure_installation
Just follow the prompts to set a password for the root user and to secure your MySQL installation.
Now if you want to access your Raspberry Pi’s MySQL server and start making changes to your databases, you can enter the following command. Not needed now
sudo mysql -u root -p

Python 2.7 required installation 
$ sudo apt-get install python-mysqldb
$ sudo apt install python-pip
$ pip install --upgrade pip
$ pip install mysql-connector-python
$ python -m pip install --upgrade pip
$ sudo apt install aircrack-ng
$ sudo apt install libcurl4-openssl-dev libssl-dev
$ pip install pycurl 

To run the program
Will run every 1 second until 50 seconds
$ sudo python main.py [device name]
$ sudo python main.py [device name] [duration]
$ sudo python main.py stop [device name]

# to run the sniffer at the raspberry startup

ifconfig
#get the current device name and replace wit wlan0

nano runWifiSniffer.sh

sudo chmod 755 ~Documents/wifi-sniffer-raspberry/runWifiSniffer.sh
cd
mkdir logs
sudo crontab -e
#select 1 or enter

@reboot sh /home/pi/Documents/wifi-sniffer-raspberry/runWifiSniffer.sh >/home/pi/logs/cronlog 2>&1

# log
cd logs
cat cronlog
