#!/bin/bash

packageList="python3-pip python3-dev"

# It's necesary run it as root to intsall packages
if [ "$EUID" -ne 0 ]
  then  echo "[-] Please run as root"
  exit
else
	echo "[+] Running as root"
fi

for pkg in $packageList; do
	dpkg -l | grep -qw $pkg || apt update && apt install -y $pkg
done

pip3 install -r requirements.txt