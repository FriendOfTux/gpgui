#!/usr/bin/python3

import os
import re
import sys
import gnupg

# CRYPTO #

user = os.getlogin()
if gnupg.__version__ < '1':					#version check because of variable name
    gpg = gnupg.GPG(gnupghome='/home/' + user + '/.gnupg')
else:
    gpg = gnupg.GPG(homedir='/home/' + user + '/.gnupg')

def generate_key(user, passphrase):				#generate a key in /home/testgpguser/.gnupg/
    input_data = gpg.gen_key_input(				#set email, passphrase, cipher, length and format
        name_email= user,
        passphrase= passphrase,
        key_type = 'RSA',
        key_length = 4096
	)
    gpg.encoding = 'UTF-8'
    key = gpg.gen_key(input_data)
    if len(str(key)) > 0:					#print fingerprint "as return statement"
        print("Fingerprint is: " + str(key))
        return True
    else:
        print("Something went wrong")
        return False

def remove_key(fingerprint, passwd):				#remove secret and public key
    print("Deleting key with fingerprint: " + fingerprint)
    del_sec = gpg.delete_keys(fingerprints=fingerprint, secret=True, passphrase=passwd).status
    print(del_sec)
    del_pub = gpg.delete_keys(fingerprints=fingerprint, secret=False).status
    print(del_pub)
    if del_pub == "ok":
        return True
    else:
        return False

def enc(msg, rec):						#enrcypt a string for a specific recipient
    res = gpg.encrypt(msg, rec)
    cipher = str(res)
    return cipher

def encrypt(file, rec):						#encrypt a file for a specific recipient
    with open(file,'rb') as f:
        status = gpg.encrypt_file(f, recipients = [rec], output=file+".encrypted")
#        print(status.ok)
#        print(status.stderr)

def dec(cipher, passwd):					#decrypt a string usign a given passsphrase
    msg = gpg.decrypt(cipher, passphrase=passwd)
    return msg

def decrypt(file, passwd):					#decrypt a file using a given passphrase
    with open(file, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase = passwd, output = file + ".decrypted")
#        print(status.ok)
#        print(status.stderr)

def sign_detached(sigFile, passwd):				#create detached signature
#    print("Signing " +sigFile+ " with " + passwd)
    with open(sigFile, "rb") as f:
        stream = gpg.sign_file(f, passphrase=passwd, detach=True, output=sigFile+".sig")
        print(stream.status)
        return stream.status

def verify_signature(file, signature):				#verify signature
    with open(signature, "rb") as sigb:
        verify = gpg.verify_file(sigb, file)
        print(verify.status)
        return verify.status


def import_key(file):						#import a key and return its uid
    old_keys = list_keys(False, 0)
    key_data = open(file).read()
    import_result = gpg.import_keys(key_data)
    gpg.trust_keys(import_result.fingerprints, 'TRUST_ULTIMATE')
    keys = list_keys(False, 0)
    key = [item for item in keys if item not in old_keys]
    if len(key) == 0:						#return last key if key was already present
        return keys[len(keys)-1]
    else:
        return key[0]

def export_key(uid):						#export public key based on email
    keys = list_keys(False, 0)
    for key in keys:
        if key == uid:						#search "key objects" for an email
            ascii_key = gpg.export_keys(key)
            with open(uid + ".pub", 'w') as file:
                file.write(ascii_key)

def list_keys(do, mode):						#list all public keys 
    keylist = gpg.list_keys()
    keys = re.findall("<(.+?)>", str(keylist))				#extract emails from key-object-list
    fingerprints = re.findall("'fingerprint': '(.+?)'", str(keylist))	#extract fingerprints "
    if do == True:
        import itertools						#use itertools to print both email and fingerprint
        for (k, f) in zip(keys, fingerprints):
            print(k, f)
    if mode == 0:							#set return values based on "mode"-value
        return keys
    elif mode == 1:
        return fingerprints
    elif mode == 2:
        return keys, fingerprints

def printLicense(cli):							#print the license of the program
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    file = open(dir + '/LICENSE', 'r')
    license = file.read()
    if cli:
        print(license)
    else:
        return license

def printInfo(cli):							#print info about the program
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    file = open(dir + '/About/Info', 'r')
    info = file.read()
    if cli:
        print(info)
    else:
        return info


# CLI #

def printHelp():							#print out a help menu for the cli
        print('Rules:\n\
-g/--generate			 		= generate key \n\
-R/--remove <fingerprint>			= remove key \n\
-d/--decrypt		   			= decrypt file with passphrase \n\
-e/--encrypt			  		= encrypt file for recipient \n\
-v/--verify <signature file>			= verifiy detached signature \n\
-s/--sign					= create detached signature \n\
-i/--import	 				= import public key\n\
-x/--export <email>				= export key from user via email \n\
-l/--list					= list key uids\n\
-f/--file <file>				= choose file \n\
-p/--passphrase <passphrase>			= choose passphrase \n\
-r/--recipient <email>				= choose recipient \n\
\n\
Examples:\n\
libgpg.py -f README -v README.sig\n\
libgpg.py -f README -r testgpguser@mydomain.com -e\n\
libgpg.py -f README.decrypted -p <passphrase> -d\n\
libgpg.py -p <passphrase> -R <fingerprint>'
)

argv = sys.argv[1:]							#use command line arguments with sys
if len(argv) > 0:							#and organize them with getopt
    import getopt							#create short and long argument list
    unixOpts = 'f:hgR:r:dev:si:x:lp:IL'
    gnuOpts = ['file=', 'help', 'generate', 'remove=', 'decrypt', 'encrypt', 'verify=', 'sign', 'import', 'export=', 'list', 'license', 'passphrase=', 'recipient=', 'info', 'license']
    try:
        opts, args = getopt.getopt(argv, unixOpts, gnuOpts)
    except:									#if argv[1], etc not in opts print 'error'
        print("Unknown Parameter")
        printHelp()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ['-f', '--file']:					#select a file
            file = arg
        elif opt in ['-p', '--passphrase']:				#select a passphrase
            passphrase = arg
        elif opt in ['-r', '--recipient']:				#select a uid
            recipient = arg
        elif opt in ['-h', '--help']:				#print help menu
            printHelp()
        elif opt in ['-g', '--generate']:				#generate a key
            uid = input("Enter Email: ")
            pw = input("Enter Passphrase: ")
            print("Generating Key for " + uid)
            generate_key(uid, pw)
        elif opt in ['-R', '--remove']:				#remove a key
            remove_key(arg, passphrase)
        elif opt in ['-d', '--decrypt']:				#decrypt a file
            if os.path.exists(file):
                print("Decrypting: "+ file)
                decrypt(file, passphrase)
            else:
                print("File not found")
        elif opt in ['-e', '--encrypt']:				#encrypt a file
            if os.path.exists(file):
                print("Encrypting: "+ file)
                encrypt(file, recipient)
            else:
                print("File not found")
        elif opt in ['-v', '--verify']:				#verify a signature
            if os.path.exists(file) and os.path.exists(arg):
                print("Verifying " + file + " with " + arg)
                verify_signature(file, arg)
            else:
                print("File not found")
        elif opt in ['-s', '--sign']:				#sign a file
            if os.path.exists(file):
                print("Signing " + file)
                sign_detached(file, passphrase)
            else:
                print("File not found")
        elif opt in ['-i', '--import']:				#import a public key
            print("Importing " + arg)
            import_key(arg)
        elif opt in ['-x', '--export']:				#export a public key
            print("Exporting " + arg)
            export_key(arg)
        elif opt in ['-l', '--list']:				
            print("List of Public Keys:")				#list public keys and fingerprints
            list_keys(True, 2)
        elif opt in ['-L', '--license']:				#print license
            printLicense(True)
        elif opt in ['I', '--info']:				#print info about the script
            printInfo(True)
