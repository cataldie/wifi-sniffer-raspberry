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

To run the program
$ sudo python main.py [device-name] 
In this case the scanning time is 50 sec, if you want a custom scanning time use the following command:
$ sudo python main.py [device-name] [scanning-time]
