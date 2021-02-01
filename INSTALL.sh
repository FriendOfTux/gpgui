#!/bin/bash

[ `id -u` -eq 0 ] && echo 'Rootcheck passed' && sleep 0.5 || (( echo 'Please call as root!' && exit ))
									#check for root privileges
printf 'Checking Distribution: ' ; sleep 0.5
Dist=$(cat /etc/*-release | grep ID_LIKE)				#checking for Distribution
[[ $Dist =~ "debian" ]] && echo "Found Debian" && act="apt install"
[[ $Dist =~ "arch" ]] && echo "Found Arch " && act="pacman -S"

dist_packages=" gpg python3-gnupg python3 python3-pip"			#apt/pacman packages ; python3-gnupg not via pip3 (std version 0.4.6)
pip_packages=" PySide6  "						#pip3 packages

sleep 0.5

echo "Installing $dist_packages"					#install packages
sudo $act $dist_packages

sleep 0.5

echo "Installing $pip_packages"						#install python side-packages
pip3 install $pip_packages
