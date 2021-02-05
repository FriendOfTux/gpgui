# gpgui
Graphical Interface for GPG

![gpgui.png](https://raw.githubusercontent.com/FriendOfTux/gpgui/main/gpgui.png)

Developed under: Pop!_OS, Arch\
Installation: see INSTALL.sh

gpgui is a script I made to teach Students about the GNU Privacy Guard. \
It is written in python and depends on "python-gnupg", "PySide6" and "gpg".\
The script offers the possibility to interact with gpg and to learn\
basics about QT-GUI's and getopt.

CAN:\
encrypt / decrypt string/file\
import / export public key\
auto-use imported key\
change recipient\
un/hide passphrase\
cli-only / gui-only mode

CAN'T (FOR NOW):\
change default user for signing\
catch text from other application\
insert text into other application\
import and save password

RESOURCES:\
gpg: 		gnupg.org\
  			digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages\
gnupg:		pythonhosted.org/gnupg/gnupg.html\
Python Qt:	dc.qt.io/qt-5/

