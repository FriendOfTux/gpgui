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
Dist=$(cat /etc/*-release | grep ID)				#check Distribution

if [[ $Dist =~ "debian" ]] ;
then
	echo "Found Debian"
	dist_packages=" gpg python3 python3-pip"			#apt packages
	echo "Installing $dist_packages"				#install packages
	sleep 0.5
	sudo apt install $dist_packages
	pipver=pip3
fi
if [[ $Dist =~ "arch" ]] ;
then
	echo "Found Arch "
	dist_packages=" gnupg python python-pip"			#pacman packages
	echo "Installing $dist_packages"				#install packages
	sleep 0.5
	sudo pacman -S $dist_packages
	pipver=pip
fi


pip_packages=" python-gnupg PySide6 pyperclip "			#pip packages
echo "Installing $pip_packages"					#install python packages
sleep 0.5
$pipver install $pip_packages

chmod +x gpgui gpgcli.py
