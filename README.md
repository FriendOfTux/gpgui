# gpgui
Graphical Interface for GPG

DATA:
uid = "testgpguser@mydomain.com"
passwd = 'my passphrase'

uid = "anothergpguser@otherdomain.com"
passwd: "other password"


CAN:
ENCRYPT STRING/FILE
DECRYPT STRING/FILE
IMPORT PUBLIC KEY
EXPORT PUBLIC KEY
AUTO-USE IMPORTED KEY
CHANGE RECIPIENT	
UN/HIDE PASSPHRASE
CLI-ONLY MODE

CANT (FOR NOW):
CHANGE DEFAULT USER FOR SIGNING
CATCH TEXT FROM OTHER GUI/CLI
INSERT TEXT INTO OTHER GUI/CLI
IMPORT AND SAVE PASSWORD (SECURE)

RESSOURCES:
gpg: 		gnupg.org
  			digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages
gnupg:		pythonhosted.org/gnupg/gnupg.html
Python Qt:	dc.qt.io/qt-5/

