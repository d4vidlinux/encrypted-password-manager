import sqlite3
import string
import secrets
from cryptography.fernet import Fernet
from pathlib import Path

# Generate Key and storage
file_path = Path("decrypt.key")

if file_path.exists():
    key = file_path.read_bytes()
else:
    key = Fernet.generate_key()
    file_path.write_bytes(key)

f = Fernet(key)


# def encryptSrc():

#     with sqlite3.connect("passwordManager.db") as conn:
#         cursor = conn.cursor()

#     for password in forEncrypt():
#         encrypted_password = f.encrypt(password.encode()).decode()
#         cursor.execute("UPDATE password_manager SET password = ?", (encrypted_password,))

#     conn.commit()

def encryptSrc():
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        items = cursor.execute("SELECT id, password FROM password_manager")
        for_encrypt = items.fetchall()

        for id, password in for_encrypt:
            token_encrypted = f.encrypt(password.encode()).decode()
            cursor.execute("UPDATE password_manager SET password = ? WHERE id = ?", (token_encrypted, id))


        conn.commit()



# def decryptSrc():

#     with sqlite3.connect("passwordManager.db") as conn:
#         cursor = conn.cursor()

#         for password in forEncrypt():
#             decrypted_password = f.decrypt(password.encode()).decode()
#             cursor.execute("UPDATE password_manager SET password = ?", (decrypted_password,))
        
def decryptSrc():

    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        items = cursor.execute("SELECT id, password FROM password_manager")
        for_decrypt = items.fetchall()

        for id, password in for_decrypt:
            token_encrypted = f.decrypt(password.encode()).decode()
            cursor.execute("UPDATE password_manager SET password = ? WHERE id = ?", (token_encrypted, id))
        
        conn.commit()




def generatePassword():
    allString = string.ascii_letters + string.digits + "!@#$%*()"
    passwordList = [secrets.choice(allString) for i in range(11)]
    return "".join(passwordList)


def createTable():
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS password_manager (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, platform TEXT NOT NULL, user TEXT NOT NULL, password TEXT NOT NULL UNIQUE)")

        conn.commit()


def createAccount(platform, user, password):
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        if not password:
            cursor.execute("INSERT INTO password_manager (platform, user, password) VALUES (?, ?, ?)", (platform, user, generatePassword()))
        else:
            cursor.execute("INSERT INTO password_manager (platform, user, password) VALUES (?, ?, ?)",(platform, user, password))

        conn.commit()


def changePassword(platform, user, password):
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        if not password:
            cursor.execute("UPDATE password_manager SET password = ? WHERE platform = ? AND user = ?", (generatePassword(), platform, user))
        else:
            cursor.execute("UPDATE password_manager SET password = ? WHERE platform = ? AND user = ?", (password, platform, user))

        conn.commit()


def deleteAccount(platform, user, password):
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM password_manager WHERE platform = ? AND user = ? AND password = ?", (platform, user, password))

        conn.commit()


def readTable():
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        items = cursor.execute("SELECT platform, user, password FROM password_manager")
        return items.fetchall()
    
def forEncrypt():
    with sqlite3.connect("passwordManager.db") as conn:
        cursor = conn.cursor()

        epass = cursor.execute("SELECT password FROM password_manager")
        return epass.fetchall()
    


        

        
