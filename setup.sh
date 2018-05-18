#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

echo "Install mariadb-server (Press [Enter] to skip)?"
read MARIADB
if [[ $MARIADB != '' ]]; then
  cat scheme.sql
  echo "Execute these SQL commands (Press [Enter] to skip)? (Adds additional database, user and tables)"
  read SQL
fi
echo "Install PhpMyAdmin (Press [Enter] to skip)?"
read PHPMYADMIN

echo "Create Tor HTTP Proxy? (Press [Enter] to skip)"
read PROXY

apt-get update
apt-get install gcc python3 python3-pip python3-mysql.connector -y

if [[ $MARIADB != '' ]]; then
  apt-get install mariadb-server -y
else
  echo "Skipping mariadb-server install"
fi

if [[ $PHPMYADMIN != '' ]]; then
  apt-get install phpmyadmin -y
else
  echo "Skipping PhpMyAdmin install"
fi

pip3 install scrapy
pip3 install service_identity --upgrade --force

if [[ $SQL != '' ]]; then
  echo "Executing SQL commands"
  mysql -u root < scheme.sql
else
  echo "Skipping SQL commands"
fi

if [[ $PROXY != '' ]]; then
  echo "Creating Tor HTTP proxy"
  apt-get install privoxy tor -y
  echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config
  systemctl restart privoxy
  # Hashed password is: secretPassword
  echo "HashedControlPassword 16:ADDFE068D133A14C605A2D0196693599B2D2DC01FC6731606D88D57ACB" >> /etc/tor/torrc
  echo "ControlPort 9051" >> /etc/tor/torrc
  systemctl restart tor
  echo "HTTP Proxy setup, port 8118"
else
  echo "Skipping Tor proxy creation"
fi
