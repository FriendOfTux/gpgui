#!/bin/bash

if [ $(id -u) -eq 0 ] ; 							#check privileges
then
	echo 'Rootcheck passed'
	sleep 0.5
else
	echo 'Please call as root!'
	exit
fi

printf 'Checking Distribution: ' ; sleep 0.5
Dist=$(cat /etc/*-release | grep ID_LIKE)				#check Distribution
[[ $Dist =~ "debian" ]] && echo "Found Debian" && act="apt install"
[[ $Dist =~ "arch" ]] && echo "Found Arch " && act="pacman -S"
sleep 0.5

dist_packages=" gpg python3-gnupg python3 python3-pip"			#apt/pacman packages ; python3-gnupg not via pip3 (std version 0.4.6)
pip_packages=" PySide6 pyperclip "					#pip3 packages


echo "Installing $dist_packages"					#install packages
sleep 0.5
sudo $act $dist_packages


echo "Installing $pip_packages"						#install python side-packages
sleep 0.5
pip3 install $pip_packages

chmod +x gpgui gpgcli.py
