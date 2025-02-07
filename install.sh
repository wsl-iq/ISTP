#!/bin/bash

clear

if [ "$(uname)" == "Linux" ]; then
    echo "[+] System: Linux"
elif [ "$(uname)" == "Android" ]; then
    if [ -d "/data/data/com.termux" ]; then
        echo "[+] System: Termux/Android"
    else
        echo "[!] This is Android but not Termux!"
    fi
else
    echo "[!] Unknown system type!"
fi

# Check if python3-venv package is installed
if ! dpkg -l | grep -q python3-venv; then
  sudo apt update -qq
  sudo apt install -y python3-venv -qq
fi

# virtualenv and install requirements
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt > /dev/null 2>&1

if [ -d "/bin" ]; then
    sudo chmod +x /bin/*
fi

if [ -d "/include" ]; then
    sudo chmod +x /include/*
fi

if [ -d "/lib/python3.11/site-packages" ]; then
    sudo chmod +x /lib/python3.11/site-packages/*
fi

if [ -d "/lib64/python3.11/site-packages" ]; then
    sudo chmod +x /lib64/python3.11/site-packages/*
fi

if [ -f "/server/index.html" ]; then
    sudo chmod +x /server/index.html
fi

if [ -f "/server/styles.css" ]; then
    sudo chmod +x /server/styles.css
fi

if [ -f "/server/script.js" ]; then
    sudo chmod +x /server/script.js
fi
