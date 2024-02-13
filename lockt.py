

import hashlib
from cryptography.fernet import Fernet
from os import listdir
from os.path import isdir

def encryption_warning_msg():
    """Pauses right before the encryption and asks the user to verify that they want to proceed with encryption. An extra step to prevent accidents."""
    while True:
        print("Remember to always create a backup of your data before encrypting it.\nDon't say that I didn't warn you.")
        print("Are you sure that you want to proceed?")
        print("[1] Yes, encrypt my file(s)\n[2] No, abort!")
        goforit = input()
        if goforit.strip() == "2" or goforit.strip() == "[2]" or goforit.lower().strip() == "no" or goforit.lower().strip() == "abort":
            print("\nOkay, aborted.")
            exit()
                        
        elif goforit.strip() == "1" or goforit.strip() == "[1]" or goforit.lower().strip() == "yes" or goforit.lower().strip() == "encrypt" or goforit.lower().strip() == "encryptmyfiles":
            print("Okay, proceeding with encryption.\n")
            break

        else:
            print("Please type one of the options to confirm or deny that you want to encrypt your directory.\n")
            continue
                        
def hash_file(path):
    """Produce a hash of the file in order to ensure file integrity and return a hex representation of the hash"""
    with open(path, "r") as f:
        file = f.read()
        hash_of_file = hashlib.sha3_512(file.encode()).hexdigest()
        return hash_of_file
      
def string_of_all_files(path):
    """Iterates through the directory, adds them all to a list, sorts them, concatenates them all together as one string using the .join() method, and returns that long string. This is use in the hashing process."""
    dirfiles = []
    for i in listdir(path):
        with open(f"{path}{i}", "r")as f:        
            x = f.read()
            dirfiles.append(str(x))
    dirfiles.sort()
    dirfiles = "".join(dirfiles)
    return dirfiles

def encrypt():
    """
    Open the file or directory, generate a key if needed, encrypt file(s), hash the file, and then print the concatenated the key and the hash to be used when decrypting 
    """
    ditch = 0
    while ditch == 0:
        print("Do you need to encrypt a single file or a directory?\n")
        print("[1] Single file\n[2] Directory\n[3] Go Back")
        pickk = input()

        try:
            if pickk.strip() == "1" or pickk.strip() == "[1]" or pickk.lower().strip() == "singlefile":
                path = input("Enter the full path name of file.\n ")
                print("If you already have a key from a previous Lockt session and would like to reuse it, enter it now. Otherwise press Enter.")
                key = input()

                if len(key) == 0: 
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    print("\n------ [INFO] " + "-" *96)
                    print("A hash will be appended directly after the key using the separator of {!!!}.")
                    print("You will need to keep these together as one long key if you want to use Lockt to decrypt your file.")
                    print("The two part key will be what Lockt excpects to see when using it to decrypt.")
                    print("You can still decrypt the file using the following key without the hash if you need to do so.")
                    print("-" *110 + "\n\n")
                    print("WARNING! THIS FILE WILL BE ENCRYPTED AND CAN ONLY BE DECRYPTED WITH THE KEY")
                    encryption_warning_msg()
                    
                elif len(key) > 0: 
                    key = key.split("!!!")
                    key = key[0]
                    key = key.encode()
                    fernet = Fernet(key)
                    print("\n------ [INFO] " + "-" *96)
                    print("Okay, your previous fernet key will be reused in this encryption.")
                    print("A hash will be appended directly after the key using the separator of {!!!}.")
                    print("You will need to keep these together as one long key if you want to use Lockt to decrypt your file.")
                    print("The two part key will be what Lockt excpects to see when using it to decrypt.")
                    print("You can still decrypt the file using the following key without the hash if you need to do so.")
                    print("If you did not make any changes to the file, you should still be able to use your same key without issues.")
                    print("If you are unsure whether you made changes or not while interacting with the file, consider saving the following key.")
                    print("-" *110 + "\n\n")
                    print("WARNING! THIS FILE WILL BE ENCRYPTED AND CAN ONLY BE DECRYPTED WITH THE KEY")
                    encryption_warning_msg()
                   
                with open(path, "rb") as f:
                    bin_file = f.read()
                    encrypted_file = fernet.encrypt(bin_file)

                with open(path, "wb") as f:
                        f.write(encrypted_file)

                hsh = hash_file(path)
                
                print("SAVE THIS KEY OR YOU WILL LOSE ACCESS TO YOUR FILE!\n")
                print(f"{key.decode()}!!!{hsh}")
                del(key)

                print("\nFinished. File has been encrypted\n")
                ditch = 1
                
                print("Are you finished with Lockt? (y/n)\n")
                answ = input()
                
                if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                    print("\nGoodbye")
                    exit()
                
                else:
                    continue

        except Exception as e:
            print("There was a problem.")
            print(repr(e))
            print("Ignore any key that may have been given. We'll try that again.\n")
            continue 
     
        try:
            if pickk.strip() == "2" or pickk.strip() == "[2]" or pickk.lower().strip() == "directory":
                path = input("Enter the full path name of the directory\n ")
                print("If you already have a key from a previous Lockt session and would like to reuse it, enter it now. Otherwise press Enter.")
                key = input()

                if len(key) == 0:
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    print("\n------ [INFO] " + "-" *96)
                    print("A hash will be appended directly after the key using the separator of {!!!}.")
                    print("You will need to keep these together as one long key if you want to use Lockt to decrypt your file.")
                    print("The two part key will be what Lockt excpects to see when using it to decrypt.")
                    print("You can still decrypt the directory using the following key without the hash if you need to do so.")
                    print("-" *110 + "\n\n")
                    print("WARNING! ALL FILES IN THE DIRECTORY WILL BE ENCRYPTED WITH A SINGLE KEY!")
                    encryption_warning_msg()
                   
                elif len(key) > 0: 
                    key = key.split("!!!")
                    key = key[0]
                    key = key.encode()
                    fernet = Fernet(key)
                    print("\n------ [INFO] " + "-" *96)
                    print("Okay, your previous fernet key will be reused in this encryption.")
                    print("A hash will be appended directly after the key using the separator of {!!!}.")
                    print("You will need to keep these together as one long key if you want to use Lockt to decrypt your files.")
                    print("The two part key will be what Lockt excpects to see when using it to decrypt.")
                    print("You can still decrypt the file using the following key without the hash if you need to do so.")
                    print("If you did not make any changes to any of the files, you should still be able to use your same key without issues.")
                    print("If you are unsure whether you made changes or not while interacting with the directory, consider saving the following key.")
                    print("-" *110 + "\n\n")
                    print("WARNING! ALL FILES IN THE DIRECTORY WILL BE ENCRYPTED WITH A SINGLE KEY!")
                    encryption_warning_msg()
                    
                def dir_encrypt_loop(path):
                    for i in listdir(path):
                        
                        if isdir(f"{path}{i}") == True:
                            dir_encrypt_loop(f"{path}{i}/")
                        else:
                            with open(f"{path}{i}", "rb") as f:
                                b_file = f.read()
                                encrypted_file = fernet.encrypt(b_file)

                            with open(f"{path}{i}", "wb") as f:
                                f.write(encrypted_file)

                dir_encrypt_loop(path)

                allfiles = string_of_all_files(path)
                allfiles = allfiles.encode()
                hsh = hashlib.sha3_512(allfiles).hexdigest()# hashes the encrypted directory so that you can see if the file has been tampered with before you decrypt it. 
                print("\nSAVE THIS KEY OR YOU WILL LOSE ACCESS TO ALL FILES IN DIRECTORY!\n")
                print(f"{key.decode()}!!!{hsh}")
                del(key)

                print("\nFinished. All files in the directory have been encrypted\n")
                ditch = 1
                
                print("Are you finished with Lockt? (y/n)\n")
                answ = input()
                
                if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                    print("\nGoodbye")
                    exit()
                
                else:
                    continue
            
        except Exception as e:
            print("There was a problem.")
            print(repr(e))
            print("Ignore any key that may have been given. We'll try that again.\n")
            continue

        if pickk.strip() == "3" or pickk.strip() == "[3]" or pickk.lower().strip() == "goback":
            ditch = 1
            continue

        else:
            print("\nWhoops!\nI didn't understand what you typed. Please choose from the options listed. Type either 1, 2, or 3.")
            continue

def decrypt(): 
    """
    Parses the key input, hashes the file, verifies the hash, and decrypts.
    """
    ditch = 0
    while ditch == 0:
        print("Do you need to decrypt a single file or a directory?")
        print("[1]  Single file\n[2]  Directory\n[3] Go Back")
        pickk = input() 

        try:
            if pickk.strip() == "1" or pickk.strip() == "[1]" or pickk.lower().strip() == "singlefile":
                path = input("Enter the full path name of file.\n ")
                key = input("Enter the key to decrypt this file.\n ")
                
                if len(key) > 0: 
                    key = key.split("!!!")
                    key_hash = key[1]
                    key = key[0]
                    key = key.encode()
                    fernet = Fernet(key)
                    hsh = hash_file(path)
                    if hsh != key_hash:
                        print("\nWARNING! THE HASH OF YOUR FILE DOESN'T MATCH THE HASH THAT WAS MADE WHEN IT WAS ENCRYPTED!\n")
                        print("This indicates that the encrypted file has changed for some reason.")
                        print("If the encrypted data has been corrupted, then decryption will fail.")
                        print("In case of failure, please restore the data from your backups")
                        print("If decryption is successfull, then the file has been altered and re-encrypted using the same key.")
                        print("If you are not aware of any change, you should discard this file and restore from backup")
                        print("Decrypting and opening this file poses a security risk.")
                        print("\nHow do you want to proceed?")
                        print("[1] Abort! Do NOT decrypt or open the file.\n[2] Decrypt anyways")
                        what = input()
                        if what.strip() == "1" or what.strip() == "[1]" or what.lower().strip() == "abort":
                            print("Okay, I will not decrypt this file.")
                            ditch = 1
                            break

                        elif what.strip() == "2" or what.strip() == "[2]" or what.lower().strip() == "decrypt":
                            print("Okay, decrypting file anyways.")
                            
                            with open(path, "rb") as f:
                                b_file = f.read()
                                decrypted_file = fernet.decrypt(b_file)

                            with open(path, "wb") as f:
                                f.write(decrypted_file)
                            
                            print("Finished. Your file has been decrypted.")
                            ditch =1

                            print("Are you finished with Lockt? (y/n)\n")
                            answ = input()
                
                            if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                                print("\nGoodbye")
                                exit()

                elif len(key) == 0:
                    print("You must enter a key in order to decrpt the file.\n Try again.")
                    continue
                

                with open(path, "rb") as f:
                    b_file = f.read()
                    decrypted_file = fernet.decrypt(b_file)

                with open(path, "wb") as f:
                    f.write(decrypted_file)
        
                print("Finished. Your file has been decrypted.")
                ditch = 1

                print("Are you finished with Lockt? (y/n)\n")
                answ = input()
                
                if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                    print("\nGoodbye")
                    exit()

        except Exception as e:
            print("There was a problem.")
            print(repr(e))
            print("We'll try that again.\n")
            continue
        
        try:
            if pickk.strip() == "2" or pickk.strip() == "[2]" or pickk.lower().strip() == "directory":
                path = input("Enter the full path name of directory.\n ")
                key = input("Enter the key to decrypt this directory.\n ")
                
                if len(key) > 0: 
                    key = key.split("!!!")
                    key_hash = key[1]
                    key = key[0]
                    key = key.encode()
                    fernet = Fernet(key)
                    allfiles = string_of_all_files(path)
                    allfiles = allfiles.encode()
                    hsh = hashlib.sha3_512(allfiles).hexdigest()

                    def dir_decrypt_loop(path, local_fernet):
                            for i in listdir(path):
                        
                                if isdir(f"{path}{i}") == True:
                                    dir_decrypt_loop(f"{path}{i}/")
                                else:
                                    with open(f"{path}{i}", "rb") as f:
                                        b_file = f.read()
                                        decrypted_file = local_fernet.decrypt(b_file)

                                    with open(f"{path}{i}", "wb") as f:
                                        f.write(decrypted_file)

                    if hsh != key_hash:
                        print("\nWARNING! THE HASH OF YOUR FILES DOESN'T MATCH THE HASH THAT WAS MADE WHEN THEY WERE ENCRYPTED!\n")
                        print("This indicates that some or all of the files have changed for some reason.")
                        print("If the encrypted data has been corrupted, then decryption will fail.")
                        print("In case of failure, please restore the data from your backups")
                        print("If decryption is successfull, the files have been altered and re-ecrypted using the same key.")
                        print("If you are not aware of any change, you should discard these files and restore from backup")
                        print("Decrypting and opening this directory poses a security risk.")
                        print("\nHow do you want to proceed?")
                        print("[1] Abort! Do NOT decrypt or open the directory.\n[2] Decrypt anyways")
                        what = input()
                        if what.strip() == "1" or what.strip() == "[1]" or what.lower().strip() == "abort":
                            print("Okay, I will not decrypt this directory.")
                            ditch = 1
                            break

                        elif what.strip() == "2" or what.strip() == "[2]" or what.lower().strip() == "decrypt":
                            print("Okay, decrypting directory anyways.")

                        dir_decrypt_loop(path, fernet)

                        print("Finished. All files in the directory have been decrypted.")
                        ditch = 1

                        print("Are you finished with Lockt? (y/n)\n")
                        answ = input()
                
                        if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                            print("\nGoodbye")
                            exit()

                elif len(key) == 0:
                    print("You must enter a key in order to decrpt the directory.\n Try again.")
                    continue
                    
                dir_decrypt_loop(path, fernet)

                print("Finished. All files in the directory have been decrypted.")
                ditch = 1

                print("Are you finished with Lockt? (y/n)\n")
                answ = input()
                
                if answ.lower().strip() == "y" or answ.lower().strip() == "yes":
                    print("\nGoodbye")
                    exit()

        except Exception as e:
            print("There was a problem.")
            print(repr(e))
            print("We'll try that again.\n")
            continue

        if pickk.strip() == "3" or pickk.strip() == "[3]" or pickk.lower().strip() == "goback":
            ditch = 1
            continue

        else:
            print("\nWhoops!\nI didn't understand what you typed. Please choose from the options listed. Type either 1, 2, or 3.")
            continue
def main():
    """The home page of the app. This is the beginning point and where you end up after each process. """
    while True:
        print('\n')
        print('         LOCKT                   ')
        print('       .-------.                 ')
        print('      / .-----. \                ')
        print('     / /       \ \               ')
        print('     | |        ||               ')
        print('     | |        ||               ')
        print('    /// ````````  \       ____       ')
        print('   |||    /^^^^^\  |     /    \      ')
        print('   |||   |  -------------  []  ---|| ')
        print('   ```\   \__^_^/  /     \____/      ')  
        print("     ```._______.'`              ")
        print("\nWelcome to Lockt.\nDo you need something encrypted or decrypted?\n")
        print("[1]  Encrypt\n[2]  Decrypt\n[3]  Exit\n")
        pick = input()
        
        if pick.strip() == "1" or pick.strip() == "[1]" or pick.lower().strip() == "encrypt":
            print("\n--Encrypt--")
            encrypt()

        elif pick.strip() == "2" or pick.strip() == "[2]" or pick.lower().strip() == "decrypt":
            print("\n--Decrypt--")
            decrypt()
        
        elif pick.strip() == "3" or pick.strip() == "[3]" or pick.lower().strip() == "exit":
            print("\n--Goodbye--")
            exit()

        else:
            print("\nWhoops!\nI didn't understand what you typed. Please choose from the options listed. Type either 1, 2, or 3.")
            continue

# This is the whole program's main loop. It calls main() and allows for exception handling in order to prevent crashes. 
while True:
    try:
        main()
    except Exception as e:
        print("There was a problem.")
        print(repr(e))
        print("Lets try that again")
        continue
