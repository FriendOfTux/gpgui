# gpgui
Graphical Interface for GPG

Developed under: Pop!_OS, Arch
Installation: see INSTALL.sh

gpgui is a script used to teach Students about the GNU Privacy Guard\
It is written in python and depends on "python-gnupg", "PySide6" and "gpg"\
The script offers the possibility to interact with gpg, as well as learn\
basics about QT-GUI's and getopt

DATA:\
uid = "testgpguser@mydomain.com"\
passwd = 'my passphrase'

uid = "anothergpguser@otherdomain.com"\
passwd: "other password"

CAN:\
encrypt / decrypt string/file\
import / export public key\
auto-use imported key\
change recipient\
un/hide passphrase\
cli-only / gui-only mode

CANT (FOR NOW):\
change default user for signing\
catch text from other application\
insert text into other application\
import and save password

RESSOURCES:\
gpg: 		gnupg.org\
  			digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages\
gnupg:		pythonhosted.org/gnupg/gnupg.html\
Python Qt:	dc.qt.io/qt-5/

