import base64
import pickle

from cryptography.fernet import Fernet
from Passwords import Passwords


class PasswordManager:
    def __init__(self):
        self.key = None
        self.passList = []
        # self.passwords = Passwords()

    def CreatePassword(self, site, username, password):
        return Passwords(site, username, password)

    def CreateKey(self):
        key = Fernet.generate_key()
        with open("Key.key", "wb") as f:
            f.write(key)
        print("[+] Created successfully")

    def LoadKey(self):

        with open("Key.key", "rb") as f:
            eenctyptedkey = f.read()
            self.key = eenctyptedkey
            print("[+] The key is loaded")
            return eenctyptedkey

    def AddPassword(self, passwrd):
        self.passList.append(passwrd)


    def ShowPasswords(self):
        for passwrd in self.passList:
            print(f"Site: {passwrd.site}, Username: {passwrd.username}, Password: {passwrd.password}")

    def DecryptFile(self):
        if self.key is None:
            print("The key is not set. Please load or create a key.")
            return
        key = pm.LoadKey()
        with open("mypass.txt", "rb") as file:

            # cipher_suite = Fernet(self.key)
            encryptedSite = b''
            encryptedusern = b''
            encryptedPass = b''
            for passinfo in file:
                passinfo = passinfo.strip().decode()  # Remove any trailing newline characters
                site, username, password = passinfo.split(" ")
                encryptedSite = site
                encryptedusern = username
                encryptedPass = password
                decryptsite = Fernet(key).decrypt(encryptedSite)
                decryptusername = Fernet(key).decrypt(encryptedusern)
                decryptpass = Fernet(key).decrypt(encryptedPass)
                passwd = Passwords(decryptsite, decryptusername, decryptpass)
                self.passList.append(passwd)

    def EncryptFile(self):
        if self.key is None:
            print("The key is not set. Please load or create a key.")
            return
        key = Fernet(self.key)
        # # cipher_suite = Fernet(self.key)
        # encrypted_list = []
        # for password in self.passList:
        #  encrypedsite = Fernet(key).encrypt(password.site.encode())
        #  encryptusern = Fernet(key).encrypt(password.username.encode())
        #  encrypedpass = Fernet(key).encrypt(password.password.encode())
        #  encryptedpassword = Passwords(encrypedsite, encryptusern, encrypedpass)
        #  encrypted_list.append(encryptedpassword)
        encrypted = b''
        # dataforPass = self.passList
        encryptedData = key.encrypt(pickle.dumps(self.passList))
        encrypted = encryptedData
        with open("mypass.txt", "wb") as file:
            file.write(encrypted)
            print("Successful encrypted")

    def loadPassFile(self):
        if self.key is None:
            print("The key is not set. Please load or create a key.")
            return

        key = Fernet(self.key)
        with open("mypass.txt", "rb") as file:
            encryptedData = file.read()

        decryptedData = key.decrypt(encryptedData)
        decryptedObjects = pickle.loads(decryptedData)  # Decode the decrypted bytes to string

        for obj in decryptedObjects:
            site = obj.get_site()
            username = obj.get_username()
            password = obj.get_password()
            passwd = Passwords(site, username, password)
            self.passList.append(passwd)

        for passwrd in self.passList:
            print(f"Site: {passwrd.site}, Username: {passwrd.username}, Password: {passwrd.password}")

    # def EncryptPassword(self, passwrd):
    #  if self.key is None:
    #   print("The key is not set. Please load or create a key.")
    #   return
    #  encrypted_site = Fernet(self.key).encrypt(passwrd.site.encode())
    #  encrypted_usrn = Fernet(self.key).encrypt(passwrd.username.encode())
    #  encrypted_pass = Fernet(self.key).encrypt(passwrd.password.encode())
    #  encrypted_password = Passwords(encrypted_site,encrypted_usrn, encrypted_pass)
    #  return encrypted_password

    # def savePasswordToFile(self, password):
    #        with open("mypass.txt", "a") as file:
    #            # cipher_suite = Fernet(self.key)
    #            encrypted_site = Fernet(self.key).encrypt(password.site)
    #            encrypted_usrn = Fernet(self.key).encrypt(password.username)
    #            encrypted_pass = Fernet(self.key).encrypt(password.password)
    #            encrypted_password = Passwords(encrypted_site,encrypted_usrn, encrypted_pass)
    #            file.write(f"{encrypted_password.site} {encrypted_password.username} {encrypted_password.password}\n")
    #        print("Password has been saved to the file.")
    def main(self):
        print(""" What do you want to do?
         1 Create a new key
         2 Load an existing key
         3 Load a Password file
         4 Add a new password
         5 Show the passwords
         q Quit
         """)

        done = False
        while not done:
            choice = input("Enter your choice: ")
            if choice == "1":
                pm.CreateKey()
            elif choice == "2":
                pm.LoadKey()
                print(pm.key)
            elif choice == "3":
                pm.loadPassFile()
                print(pm.passList)
            elif choice == "4":
                site = input("Enter Site: ")
                usern = input("Enter Username: ")
                pasdr = input("Enter Password: ")
                pas = pm.CreatePassword(site, usern, pasdr)
                # encrpass = pm.EncryptPassword(pas)
                pm.AddPassword(pas)
                # pm.savePasswordToFile(encrpass)
            elif choice == "5":
                # pm.DecryptFile()
                pm.ShowPasswords()
            elif choice == "q":
                pm.EncryptFile()
                print("Bye")
                done = True2
            elif choice == "":
                print("Please select one of the options!")


pm = PasswordManager()

if __name__ == '__main__':
    pm.main()
