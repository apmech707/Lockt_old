**UPDATE**
I have become aware of a limitation of using fernet with large files. I am in the process of rewriting this code
using the cryptography library using symmetric encryption a different way. This app should stil work now, but if you 
have a large file to encrypt please test this first before using it. source for info is here - https://cryptography.io/en/latest/fernet/#limitations.




Lockt

This is a program that can encrypt or decrypt a file, or directory of files using the cryptography.fernet module. It is a command line interface app. This code is optomized for a linux file system, however the ability for this to be run on a windows file system could be added relatively easily. 

-DISCLAIMER-

This app has the ability to encrypt entire directories including all the files within them. Reckless use of the app could easily result in total loss of your data. It is your responsibility to ensure that you verify the correct path of the data to be encrypted before you proceed, and that you save the key so that you can decrypt you data. I am not responsible for any loss of data as a result of using this software. Look over the code and become familiar with it before you use it if your data is irreplaceable. I added safeguards to prevent accidents as best that I could, but you the user are always expected to have critical thinking and restraint while using encyption software. ALWAYS CREATE A BACKUP OF YOUR DATA BEFORE ENCRYPTING IT. You have been warned, and are now free to enjoy the benfits of easy to use, secure, and open-source encryption. 

CIA TRIAD

Confidentiality:
This program encrypts your data using the python module cryptography.fernet which uses AES 128 encryption.

Integrity:
Data integrity is ensured using the python hashlib module. Hashing is done with the SHA3_512 algorithm, and the result is added to your key. This is checked and verified for integrity directly before decryption.
        
Availability:
The easy to use interface, the ability to reuse the same key when you re-encrypt, and seamless exception handling allows for fast and intuitive access to your data. This gives you the best access to your data that I could manage while still offering tight security.
        
        
