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
$ pip install mysql-connector-python
