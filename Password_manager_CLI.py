#!/usr/bin/env python3

from cryptography.fernet import Fernet
from pathlib import Path
import sqlite3
import secrets
import string

# Title
print("="*6, " Password Manager CLI","="*6)


## Generate Key and storage
file_path = Path("decrypt.key")

if file_path.exists():
    key = file_path.read_bytes()
else:
    key = Fernet.generate_key()
    file_path.write_bytes(key)

f = Fernet(key)


## Create table "account_manager"
def create_table():
     with sqlite3.connect("account.db") as connect:
        cursor = connect.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS account_manager (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, platform TEXT NOT NULL, user TEXT NOT NULL, password TEXT NOT NULL UNIQUE)")

        connect.commit()



## Generate auto password
def create_password(length: int):
    characters = string.ascii_letters + string.digits + "!@#$%*()"
    password_list = [secrets.choice(characters) for i in range(length)]
    return "".join(password_list)


new_password = create_password(10)



## Save account
def save_account(platform, user, password):
    create_table()
    with sqlite3.connect("account.db") as connect:
        cursor = connect.cursor()

        if not password.strip():
            cursor.execute("INSERT INTO account_manager (platform, user, password) VALUES (?, ?, ?)", (platform, user, new_password))

        else:
            cursor.execute("INSERT INTO account_manager (platform, user, password) VALUES (?, ?, ?)", (platform, user, password))

        connect.commit()

        return True


## Change password
def update_account(platform, user, password):
    create_table()
    with sqlite3.connect("account.db") as connect:
        cursor = connect.cursor()

        if not password:
            cursor.execute("UPDATE account_manager SET password = ? WHERE platform = ? AND user = ?", (new_password, platform, user))

        else:
            cursor.execute("UPDATE account_manager SET password = ? WHERE platform = ? AND user = ?", (password, platform, user))

        connect.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False


## Delete account
def remove_account(platform, user):
    with sqlite3.connect("account.db") as connect:
        cursor = connect.cursor()

        cursor.execute("DELETE FROM account_manager WHERE platform = ? AND user = ?", (platform, user))

        connect.commit()
        return True
    

## Print table items
def show():
    try:
        with sqlite3.connect("account.db") as connect:
            cursor = connect.cursor()

            cursor.execute("SELECT * FROM account_manager")
            results = cursor.fetchall()
            
            for line in results:
                print(f"Platform: {line[1]} | Username: {line[2]} | Password: {line[3]}")
    except sqlite3.OperationalError:
        print("Error: Table 'account_manager' was not founded!")



## Encrypt
def encrypt_src():
    try:
        with sqlite3.connect("account.db") as connect:
            cursor = connect.cursor()

            items = cursor.execute("SELECT * FROM account_manager")
            for_encrypt = items.fetchall()

            for token in for_encrypt:
                token_encrypted = f.encrypt(token[3].encode()).decode()
                cursor.execute("UPDATE account_manager SET password = ?", (token_encrypted,))


            connect.commit()
    except sqlite3.OperationalError:
        print("Error: Table account_manager was not founded!")


## Decrypt
def decrypt_src():
    try:
        with sqlite3.connect("account.db") as connect:
            cursor = connect.cursor()

            items = cursor.execute("SELECT * FROM account_manager")
            for_decrypt = items.fetchall()

            i = 1
            for token in for_decrypt:
                token_decrypted = f.decrypt(token[3].encode()).decode()
                cursor.execute("UPDATE account_manager SET password = ? WHERE id = ?", (token_decrypted,i))
                i += 1
            
            connect.commit()
    except sqlite3.OperationalError:
        print("Error: Table account_manager was not founded!")


## Interface
while True:
    print("""
          1 - Create account
          2 - Update account
          3 - Remove account
          4 - View table
          5 - Encrypt data
          6 - Decrypt data
          0 - Exit
          """)

    ask = input("What you need?\n> ")

    if ask == "1":
        platform = input("Platform: ")
        user = input("User: ")
        password = input("Password: ")

        if save_account(platform=platform, user=user, password=password):
            print("Account saved!")

        else:
            print("Error in try save the account...")

    elif ask == "2":
        platform = input("Platform: ")
        user = input("User: ")
        password = input("Password: ")

        if update_account(platform=platform, user=user, password=password):
            print("Account updated!")

        else:
            print("Error in try save the account...")

    elif ask == "3":
        platform = input("Platform: ")
        user = input("User: ")

        if remove_account(platform=platform, user=user):
            print("Account successful deleted!")

        else:
            print("Error in try remove account...")

    
    elif ask == "4":
        show()


    elif ask == "5":
        encrypt_src()

    elif ask == "6":
        decrypt_src()

    elif ask == "0":
        print("Leaving...")
        break

    else:
        print("Select a valid option!")
