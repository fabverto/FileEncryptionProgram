import tkinter as tk
from tkinter import font as tkFont
from tkinter import filedialog
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os

HEIGHT = 400
WIDTH = 300

root = tk.Tk()
root.title("Encryption Program")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

encryptionFilePath = ""
decryptionFilePath = ""

'''
entry1 = tk.StringVar
entry2 = tk.StringVar
'''

titleFont = tkFont.Font(family='Helvetica', size=14, weight='bold')
optionsFont = tkFont.Font(family='Helvetica', size=9, weight='bold')
mainBtnFont = tkFont.Font(family='Helvetica', size=12, weight='bold')
btnFont = tkFont.Font(family='Helvetica', size=10, weight='bold')
helv8 = tkFont.Font(family='Helvetica', size=8, weight='bold')
helv6 = tkFont.Font(family='Helvetica', size=6)
errorFont = tkFont.Font(family='Helvetica', size=8, weight='bold')
filePathFont = tkFont.Font(family='Helvetica', size=7, weight='bold')


def _from_rgb(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

def takeInput(input):
    return input.get()

def keyGen(pwd):
    password = pwd.encode()

    mysalt = #add your salt here!

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256, length=32, salt=mysalt, iterations=1000000, backend=default_backend())

    return base64.urlsafe_b64encode(kdf.derive(password))

# ------------------------------------------------------------------------------------- Check Inputs -------------------------------------------------------------------------------------
def checkEncryption(p, p1, file, frame, top):
    psw = takeInput(p)
    psw1 = takeInput(p1)

    filePathLable = tk.Label(top, font=filePathFont, text=file).place(relx=0.005, rely=0.55, relwidth=0.995,relheight=0.04)

    #print("Password 1 is: " + psw + "\n")
    #print("Password 2 is: " + psw1 + "\n")
    #print("File Path 1 is: " + file + "\n")

    if psw == "" and psw1 == "" and file == "":
        #print("Missing Passwords and File Path")
        errormsg = tk.Label(frame, text="Missing Passwords and File Path", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    elif psw == "" or psw1 == "":
        #print("Password Missing")
        errormsg = tk.Label(frame, text="Password Missing", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    elif file == "":
        #print("File Path Missing")
        errormsg = tk.Label(frame, text="File Path Missing", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    elif psw != psw1:
        #print("Passwords Don't Match")
        errormsg = tk.Label(frame, text="Passwords Don't Match", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    else:
        encrypt(psw, frame)


def checkDecryption(p, file, frame,  top):
    psw = takeInput(p)

    #print("Password is: " + psw + "\n")
    #print("File Path 1 is: " + file + "\n")

    filePathLable = tk.Label(top, font=helv8, text=file).place(relx=0.005, rely=0.55, relwidth=0.995, relheight=0.04)

    if psw == "" and file == "":
        #print("Missing Password and File Path")
        errormsg = tk.Label(frame, text="Missing Password and File Path", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    elif psw == "":
        #print("Password Missing")
        errormsg = tk.Label(frame, text="Password Missing", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    elif file == "":
        #print("File Path Missing")
        errormsg = tk.Label(frame, text="File Path Missing", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
    else:
        decrypt(psw, frame)

#  ------------------------------------------------------------------------------------- Encrypt/Decrypt -------------------------------------------------------------------------------------
def encrypt(psw, top):

    global encryptionFilePath

    key = keyGen(psw)
    cipher = Fernet(key)

    encryptedFileName = appendId(encryptionFilePath)

    with open(encryptionFilePath, 'rb') as f:
        e_file = f.read()

    encypted_file = cipher.encrypt(e_file)

    with open(encryptedFileName, 'wb') as ef:
        ef.write(encypted_file)

    os.remove(encryptionFilePath)
    encryptionFilePath = ""

    errormsg = tk.Label(top, text="Encryption Complete", bg="white", font=errorFont).place(relx=0.05, rely=0.5,relwidth=0.95, relheight=0.2)


def decrypt(psw2, top):
    global decryptionFilePath

    key = keyGen(psw2)
    cipher = Fernet(key)

    with open(decryptionFilePath, 'rb') as df:
        encrypted_data = df.read()

    try:
        decrypted_file = cipher.decrypt(encrypted_data)
        if decryptionFilePath.find("_encrypted") != -1:
            decryptedFileName = decryptionFilePath.replace("_encrypted", "")
            #print(decryptedFileName)
        else:
            decryptedFileName = decryptionFilePath

        with open(decryptedFileName, 'wb') as df:
            df.write(decrypted_file)

        os.remove(decryptionFilePath)
        decryptionFilePath = ""

        errormsg = tk.Label(top, text="Decryption Complete", bg="white", font=errorFont).place(relx=0.05, rely=0.5,relwidth=0.95,relheight=0.2)

    except Exception as e:
        errormsg = tk.Label(top, text="Incorrect Password", bg="white", fg="red", font=errorFont).place(relx=0.05, rely=0.5, relwidth=0.95, relheight=0.2)
        #print("Password not matching:")


# ------------------------------------------------------------------------------------- Windows -------------------------------------------------------------------------------------
def encryptionWindow():

    btnEncryption["state"] = "disabled"
    btnDecryption["state"] = "disabled"

    top = tk.Toplevel(bg=_from_rgb((179, 192, 196)), height=HEIGHT, width=WIDTH)

    encryptionTitle = tk.Label(top, text="Encryption", font=titleFont, bg=_from_rgb((179, 192, 196))).place(relx=0.3, rely=0, relwidth=0.4, relheight=0.1)

    psw1entry = tk.Entry(top, font="8", bd=3)
    psw1entry.place(relx=0.25, rely=0.17, relwidth=0.7, relheight=0.08)
    psw1lable = tk.Label(top, text="Enter \n Password", bg=_from_rgb((179, 192, 196))).place(relx=0.02, rely=0.15, relwidth=0.18, relheight=0.1)

    psw2entry = tk.Entry(top, font="8", bd=3)
    psw2entry.place(relx=0.25, rely=0.31, relwidth=0.7, relheight=0.08)
    psw2lable = tk.Label(top, text="Re-Enter \n Password", bg=_from_rgb((179, 192, 196))).place(relx=0.02, rely=0.3, relwidth=0.2, relheight=0.1)

    errorFrame = tk.Frame(top, bg="white")
    errorFrame.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.15)
    frameTitle = tk.Label(errorFrame, text="DIALOG", font=helv8, bg="white").place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.15)

    fileBtn = tk.Button(top, text="File Search", font=btnFont, bd=5, command=lambda: openEncryptionFile(top)).place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.08)

    encryptBtn = tk.Button(top, text="Encrypt", font=mainBtnFont, bg="yellow", bd=5, command=lambda: checkEncryption(psw1entry, psw2entry, encryptionFilePath, errorFrame, top)).place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)

    top.protocol("WM_DELETE_WINDOW", lambda: onClosing(top))


def decryptionWindow():

    btnEncryption["state"] = "disabled"
    btnDecryption["state"] = "disabled"

    top = tk.Toplevel(bg=_from_rgb((179, 192, 196)), height=HEIGHT, width=WIDTH)

    decryptionTitle = tk.Label(top, text="Decryption", font=titleFont, bg=_from_rgb((179, 192, 196))).place(relx=0.3, rely=0, relwidth=0.4, relheight=0.1)

    pswEntry = tk.Entry(top, font="8", bd=3) #, textvariable=decryptionFilePath)
    pswEntry.place(relx=0.25, rely=0.17, relwidth=0.7, relheight=0.08)
    pswLable = tk.Label(top, text="Enter \n Password", bg=_from_rgb((179, 192, 196))).place(relx=0.02, rely=0.15, relwidth=0.18, relheight=0.1)

    errorFrame = tk.Frame(top, bg="white")
    errorFrame.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.15)
    frameTitle = tk.Label(errorFrame, text="DIALOG", font=helv8, bg="white").place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.15)

    fileBtn = tk.Button(top, text="File Search", font=btnFont, bd=5, command=lambda: openDecryptionFile(top)).place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.08)
    decryptBtn = tk.Button(top, text="Decrypt", font=mainBtnFont, bg="yellow", bd=5, command=lambda: checkDecryption(pswEntry, decryptionFilePath, errorFrame, top)).place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)

    top.protocol("WM_DELETE_WINDOW", lambda: onClosing(top))

# ------------------------------------------------------------------------------------- Open Files -------------------------------------------------------------------------------------
def openEncryptionFile(top):
    global encryptionFilePath
    encryptionFilePath = filedialog.askopenfilename(initialdir="~", title="Select a file to encrypt", filetypes=[('All files', '*.*')])
    filePathLable = tk.Label(top, font=filePathFont, text=encryptionFilePath).place(relx=0.005, rely=0.55, relwidth=0.995, relheight=0.04)

def openDecryptionFile(top):
    global decryptionFilePath
    decryptionFilePath = filedialog.askopenfilename(initialdir="~", title="Select a file to decrypt", filetypes=[('All files', '*.*')])
    filePathLable = tk.Label(top, font=filePathFont, text=decryptionFilePath).place(relx=0.005, rely=0.55, relwidth=0.995, relheight=0.04)

def appendId(filename):
    name, ext = os.path.splitext(filename)
    newName = name + "_encrypted" + ext
    return newName

def onClosing(top):
    btnEncryption["state"] = "normal"
    btnDecryption["state"] = "normal"
    top.destroy()


# ------------------------------------------------------------------------------------- Main -------------------------------------------------------------------------------------
titleFrame = tk.Frame(root, bg=(_from_rgb((36, 255, 153))))
titleFrame.place(relx=0, rely=0, relwidth=1, relheight=0.5)


title = tk.Label(titleFrame, text="Encryption/Decryption Program", bg="black", fg="white", font=titleFont)
title.place(relx=0, rely=0.1, relwidth=1, relheight=0.15)

optionlbl = tk.Label(titleFrame, text="Select one of the options below", bg=(_from_rgb((36,255,153))), font=optionsFont)
optionlbl.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.2)

buttonFrame = tk.Frame(root, bg="grey")
buttonFrame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

btnEncryption = tk.Button(buttonFrame, text="Encrypt", font=mainBtnFont, command=encryptionWindow, bg=(_from_rgb((36,205,255))))
btnDecryption = tk.Button(buttonFrame, text="Decrypt", font=mainBtnFont, command=decryptionWindow)
btnEncryption.place(relx=0.05, rely=0.1, relwidth=0.45, relheight=0.8)
btnDecryption.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.8)

root.mainloop()
