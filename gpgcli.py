#!/usr/bin/python3

import os
import re
import sys
import gnupg

user = os.getlogin()
if gnupg.__version__ < '1':  # version check
    gpg = gnupg.GPG(gnupghome='/home/' + user + '/.gnupg')
else:
    gpg = gnupg.GPG(homedir='/home/' + user + '/.gnupg')


def generate_key(user_mail, passwd):  # generate a key in /home/<username>/.gnupg/
    input_data = gpg.gen_key_input(  # set email, passphrase, cipher, length and format
        name_email=user_mail,
        passphrase=passwd,
        key_type='RSA',
        key_length=4096
    )
    gpg.encoding = 'UTF-8'
    key = gpg.gen_key(input_data)
    if len(str(key)) > 0:  # print fingerprint "as return statement"
        print("Fingerprint is: " + str(key))
        return True
    else:
        print("Something went wrong")
        return False


def remove_key(fingerprint, passwd):  # remove secret and public key
    print("Deleting key with fingerprint: " + fingerprint)
    del_sec = gpg.delete_keys(fingerprints=fingerprint, secret=True, passphrase=passwd).status
    print(del_sec)
    del_pub = gpg.delete_keys(fingerprints=fingerprint, secret=False).status
    print(del_pub)
    if del_pub == "ok":
        return True
    else:
        return False


def enc(msg, rec):  # encrypt a string for a specified recipient
    res = gpg.encrypt(msg, rec)
    cipher = str(res)
    return cipher


def encrypt(text_file, rec):  # encrypt a file for a specified recipient
    with open(text_file, 'rb') as f:
        gpg.encrypt_file(f, recipients=[rec], output=text_file + ".encrypted")


def dec(cipher, passwd):  # decrypt a string using a given passphrase
    msg = gpg.decrypt(cipher, passphrase=passwd)
    return msg


def decrypt(encrypted_file, passwd):  # decrypt a file using a given passphrase
    with open(encrypted_file, 'rb') as f:
        gpg.decrypt_file(f, passphrase=passwd, output=encrypted_file + ".decrypted")


def sign_detached(signature_file, passwd):  # create a detached signature
    with open(signature_file, "rb") as f:
        stream = gpg.sign_file(f, passphrase=passwd, detach=True, output=signature_file + ".sig")
        print(stream.status)
        return stream.status


def verify_signature(signed_file, signature_file):  # verify signature
    with open(signature_file, "rb") as signature:
        verify = gpg.verify_file(signature, signed_file)
        print(verify.status)
        return verify.status


def import_key(key_file):  # import a key and return its uid
    old_keys = list_keys(False, 0)
    key_data = open(key_file).read()
    import_result = gpg.import_keys(key_data)
    gpg.trust_keys(import_result.fingerprints, 'TRUST_ULTIMATE')
    keys = list_keys(False, 0)
    key = [item for item in keys if item not in old_keys]
    if len(key) == 0:  # return last key if key was already present
        return keys[len(keys) - 1]
    else:
        return key[0]


def export_key(user_name):  # export public key based on email
    keys = list_keys(False, 0)
    for key in keys:
        if key == user_name:  # search "key objects" for an email
            ascii_key = gpg.export_keys(key)
            with open(user_name + ".pub", 'w') as key_file:
                key_file.write(ascii_key)


def list_keys(do, mode):  # list all public keys
    key_list = gpg.list_keys()
    keys = re.findall("<(.+?)>", str(key_list))  # extract emails from key-object-list
    fingerprints = re.findall("'fingerprint': '(.+?)'", str(key_list))  # extract fingerprints
    if do:
        import itertools  # use itertools to print both email and fingerprint
        for (k, f) in zip(keys, fingerprints):
            print(k, f)
    if mode == 0:  # set return values based on "mode"-value
        return keys
    elif mode == 1:
        return fingerprints
    elif mode == 2:
        return keys, fingerprints


def print_license(cli):  # print the license of the program
    directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    info_file = open(directory + '/About/License/LICENSE', 'r')
    project_license = info_file.read()
    if cli:
        print(project_license)
    else:
        return project_license


def print_info(cli):  # print information about the program
    directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    info_file = open(directory + '/About/Info', 'r')
    info = info_file.read()
    if cli:
        print(info)
    else:
        return info


def print_help():  # print out a help menu for the cli
    print('Rules:\n\
-g/--generate			 	= generate key \n\
-R/--remove <fingerprint>		= remove key \n\
-d/--decrypt		   		= decrypt file with passphrase \n\
-e/--encrypt			  	= encrypt file for recipient \n\
-v/--verify <signature file>		= verify detached signature \n\
-s/--sign				= create detached signature \n\
-i/--import	 			= import public key\n\
-x/--export <email>			= export key from user via email \n\
-l/--list				= list keys\n\
-f/--file <file>			= choose file \n\
-p/--passphrase <passphrase>		= choose passphrase \n\
-r/--recipient <email>			= choose recipient \n\
\n\
Examples:\n\
gpgcli.py -f README -v README.sig\n\
gpgcli.py -f README -r testgpguser@mydomain.com -e\n\
gpgcli.py -f README.decrypted -p <passphrase> -d\n\
gpgcli.py -p <passphrase> -R <fingerprint>'
          )


argv = sys.argv[1:]  # use command line arguments with sys
if len(argv) > 0:  # and organize them with getopt
    import getopt  # create short and long argument list
    unixOpts = 'f:hgR:r:dev:si:x:lp:IL'
    gnuOpts = ['file=', 'help', 'generate', 'remove=', 'decrypt', 'encrypt', 'verify=', 'sign', 'import', 'export=',
               'list', 'license', 'passphrase=', 'recipient=', 'info', 'license']
    try:
        opts, args = getopt.getopt(argv, unixOpts, gnuOpts)
    except getopt.GetoptError as err:  # if argv[1], etc not in opts print error message
        print(err)
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-f', '--file']:  # select a file
            file = arg
        elif opt in ['-p', '--passphrase']:  # select a passphrase
            passphrase = arg
        elif opt in ['-r', '--recipient']:  # select a uid
            recipient = arg
        elif opt in ['-h', '--help']:  # print help menu
            print_help()
        elif opt in ['-g', '--generate']:  # generate a key
            uid = input("Enter Email: ")
            pw = input("Enter Passphrase: ")
            print("Generating Key for " + uid)
            generate_key(uid, pw)
        elif opt in ['-R', '--remove']:  # remove a key
            try:
                remove_key(arg, passphrase)
            except NameError:
                print("Passphrase is not defined")
        elif opt in ['-d', '--decrypt']:  # decrypt a file
            try:
                if os.path.exists(file):
                    print("Decrypting: " + file)
                    decrypt(file, passphrase)
                else:
                    print("File not found")
            except NameError:
                print("File is not defined")
        elif opt in ['-e', '--encrypt']:  # encrypt a file
            try:
                if os.path.exists(file):
                    print("Encrypting: " + file)
                    encrypt(file, recipient)
                else:
                    print("File not found")
            except NameError:
                print("File or Recipient is not defined")
        elif opt in ['-v', '--verify']:  # verify a signature
            if os.path.exists(file) and os.path.exists(arg):
                print("Verifying " + file + " with " + arg)
                verify_signature(file, arg)
            else:
                print("File not found")
        elif opt in ['-s', '--sign']:  # sign a file
            if os.path.exists(file):
                print("Signing " + file)
                sign_detached(file, passphrase)
            else:
                print("File not found")
        elif opt in ['-i', '--import']:  # import a public key
            print("Importing " + arg)
            import_key(arg)
        elif opt in ['-x', '--export']:  # export a public key
            print("Exporting " + arg)
            export_key(arg)
        elif opt in ['-l', '--list']:
            print("List of Public Keys:")  # list public keys and fingerprints
            list_keys(True, 2)
        elif opt in ['-L', '--license']:  # print license
            print_license(True)
        elif opt in ['-I', '--info']:  # print info about the script
            print_info(True)
