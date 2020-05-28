Simple Encryption/Decryption Python Program that lets the user encrypt and decrypt a file using SHA-256 <br />
The encrypted file is rename to: filename + "_encrypted" in the same location it was selected from.

a salt needs to be added as a byte object, in the code this must be inserted in the "mysalt" variable, you can create one with <br /> "os.urandom(16)" in your python shell

log window gives notice to the user of any errors:<br />
-wrong password<br />
-blank password<br />
-mismatching passwords<br />
-no file selected<br />

![](img/e1.PNG)<br />
Main menu at program start, can click on either encrypt or decrypt button


![](img/e2.PNG)<br />
If a button is clicked a new window pops up which disables the encryption/decryption buttons from the main menu


![](img/e3.PNG)<br />
if the "encrypt" button is clicked without providing password and path to file an error will be printed to the log box


![](img/e4.PNG)<br />
if the "encrypt" button is clicked without providing the second password and path to file an error will be printed to the log box


![](img/e5.PNG)<br />
if the "encrypt" button is clicked without providing the path to file an error will be printed to the log box


![](img/e6.PNG)<br />
a select file window will open up if the file button is clicked

![](img/e8.PNG)<br />
contents of the text file selected

![](img/e10.PNG)<br />
file path selected

![](img/e11.PNG)<br />
if the "encrypt" button is clicked and the two paswords mismatch an error will be printed to the log box

![](img/e12.PNG)<br />
encryption succesful message
![](img/e13.PNG)<br />
contents of encrypted file

![](img/e14.PNG)<br />
error message displayed if decryption password doesn't match password used for encryption

![](img/e15.PNG)<br />
decryption complete

![](img/e16.PNG)<br />
contents of decrypted file
