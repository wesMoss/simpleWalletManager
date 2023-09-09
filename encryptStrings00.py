import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
#import getpass
from easygui import passwordbox

pj = os.path.join

def exists(path):
    return os.access(path, os.F_OK)


class myCrypt:
    def __init__(self, encoding='UTF-16'):
        self.encoding = encoding
        self.salt = None
        self.iterations = None
        self.fernet = None

    def createSaltFile(self, fileName, iterations=5000000):
        self.salt = os.urandom(16)
        salt = str(self.salt, self.encoding)
        if exists(fileName):
            ans = input('Salt file '+fileName+' exists! aborting')
            exit()
        with open(fileName, 'w') as f:
            f.write(salt + '\n')
            f.write(str(iterations) + '\n')
            f.write(self.encoding)

    def loadSaltFile(self, fileName):
        with open(fileName, 'r') as f:
            temp = f.readline()
            #alternate: self.salt = bytes(temp, encoding=self.encoding)
            self.iterations = int(f.readline())
            self.encoding = f.readline()  #will overwrite encoding given at initialization
            self.salt = temp.encode(encoding=self.encoding)

    def createInternalKey(self):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256,
                         length=32,
                         salt=self.salt,
                         iterations=self.iterations,
                         backend=default_backend())
        pwLoaded = False
        while not pwLoaded:
            password = passwordbox('password:')  #getpass.getpass('input password : ')
            if len(password) < 8:
                print('must be at least 8 characters')
            else:
                pwLoaded = True
                print('got it\n')
        password = password.encode(encoding='UTF-16')
        temp = kdf.derive(password)
        key = base64.urlsafe_b64encode(temp)
        self.fernet = Fernet(key)

    def encryptString(self, message):
        if self.fernet is None:
            print('internal key not created yet!!')
            exit()
        else:
            return self.fernet.encrypt(message.encode(encoding=self.encoding)).decode(encoding=self.encoding)

    def decryptString(self, encryptedString):
        if self.fernet is None:
            print('internal key not created yet!!')
            exit()
        else:
            return self.fernet.decrypt(encryptedString.encode(encoding=self.encoding)).decode(encoding=self.encoding)


if __name__ == "__main__":
    pass
    # mc = myCrypt()

    # saltFile = pj('data', 'wallets', 'saltFile.txt')
    # #mc.createSaltFile(saltFile) #DO NOT OVERWRITE

    # mc.loadSaltFile(saltFile)
    # mc.createInternalKey()

    # oldWalletsFile = pj('data', 'wallets.txt')
    # newWalletsFile = pj('data', 'wallets', 'wallets.txt')
    # #
    # # fOld = open(oldWalletsFile, 'r')
    # # fNew = open(newWalletsFile, 'w')
    # #
    # # for line in fOld:
    # #     newLine = mc.encryptString(line)
    # #     fNew.write(newLine + '\n')
    # #
    # # fOld.close()
    # # fNew.close()

    # fNew = open(newWalletsFile, 'r')
    # for line in fNew:
    #     print(mc.decryptString(line).split())
    # fNew.close()



