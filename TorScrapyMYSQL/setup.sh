#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update
apt-get install gcc mariadb-server python3 python3-pip privoxy tor python3-mysql.connector -y
# (recommended) Optionally you can use the PHPMyAdmin interface to view your MYSQL data via web interface
apt-get install phpmyadmin -y
pip3 install scrapy
pip3 install bs4
pip3 install html2text
pip3 install stem

echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config
systemctl restart privoxy

# Hashed password is: secretPassword
echo "HashedControlPassword 16:ADDFE068D133A14C605A2D0196693599B2D2DC01FC6731606D88D57ACB" >> /etc/tor/torrc
echo "ControlPort 9051" >> /etc/tor/torrc
systemctl restart tor

# setup DB tables
mysql -u root < sqlTable.sql
pip3 install service_identity --upgrade --force

echo "You can now start TorScrapyMYSQL from here by this command:  scrapy crawl TorScrapyMYSQL"
