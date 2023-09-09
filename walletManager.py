from encryptStrings00 import myCrypt
import easygui, os, eth_account, random


def exists(path):
    return os.access(path, os.F_OK)

pj = os.path.join

class walletManager:
    def __init__(self, walletDir):
        self.walletsInfo = {}
        self.walletDir = walletDir
        if not exists(self.walletDir):
            os.makedirs(self.walletDir)
    
    def changeDirectory(self, newDir):
        self.walletDir = newDir

    def createSaltFile(self, fileName, iterations=5000000):
        saltFile = pj(self.walletDir, fileName)
        if exists(saltFile):
            print('salt file already exists. aborting.')
            exit()
        mc = myCrypt()
        mc.createSaltFile(fileName=saltFile, iterations=iterations)
        
    def getPublicKey(self, walletName):
        return self.walletsInfo[walletName][0]
        
    def getPrivateKey(self, walletName):
        temp = self.walletsInfo[walletName]
        if len(temp) == 2:
            return temp[1]
        else:
            mc = temp[2]
            return mc.decryptString(temp[1])
            
    #use saltFileName = '' for unencrypted wallet
    def openWalletFile(self, walletFileName:str, saltFileName:str = ''):
        self.walletsInfo = {}
        wallet = pj(self.walletDir, walletFileName)
        if saltFileName != '':
            saltFile = pj(self.walletDir, saltFileName)
            mc = myCrypt()
            mc.loadSaltFile(saltFile)
            mc.createInternalKey()

            with open(wallet, 'r') as wf:
                for line in wf:
                    #name, address, pk = self.mc.decryptString(line).strip().split(',')
                    name,address,pk = line.strip().split(',')
                    if name in self.walletsInfo:
                        print(name, 'already in dictionary. aborting.')
                        _ = input('...')
                        exit()  
                    #pk = self.mc.encryptString(pk)
                    self.walletsInfo[name] = [address, pk, mc]
        else:
            with open(wallet, 'r') as wf:
                for line in wf:
                    name,address,pk = line.strip().split(',')
                    if name in self.walletsInfo:
                        print(name, 'already in dictionary. aborting.')
                        _ = input('...')
                        exit()
                    self.walletsInfo[name] = [address, pk]

    def addWalletInfoToWalletFileManual(self, walletFileName:str, saltFileName:str):
        saltFile = pj(self.walletDir, saltFileName)
        walletFile = pj(self.walletDir, walletFileName)
        if not exists(saltFile):
            print('salt file not found. aborting.')
            exit()

        mc = myCrypt()
        mc.loadSaltFile(saltFile)
        mc.createInternalKey()
        if exists(walletFile):
            openMode = 'a'
        else:
            openMode = 'w'
        title = 'wallet info'
        msg = 'enter wallet info'
        fieldNames = ['wallet name', 'wallet address', 'private key']
        with open(walletFile, openMode) as wf:
            done = False
            while not done:
                name,address,pk = easygui.multenterbox(msg, title, fieldNames)
                pk = mc.encryptString(pk)
                if name not in self.walletsInfo:
                    self.walletsInfo[name] = [address, pk, mc]
                    wf.write(','.join([name,address,pk]) + '\n')
                else:
                    easygui.msgbox('that name already exists in the wallet dictionary. not adding wallet.')

                done = easygui.ynbox('all done?')
    
    def generateKeyPair(self):
        acct = eth_account.Account.create(os.urandom(random.randint(600, 1000)).hex())
        pk = acct.privateKey.hex()
        address = acct.address
        return address, pk

    def createNewWalletsAutoGenerate(self, walletFileName:str, 
                                     saltFileName:str, numberOfWallets:int, 
                                     walletNamePrefix='wallet-'):
        walletFile = pj(self.walletDir, walletFileName)
        walletEncrypted = True

        if saltFileName=='': #unencryptedWallet
            walletEncrypted = False
        else:
            saltFile = pj(self.walletDir, saltFileName)
            mc = myCrypt()
            if exists(saltFile):
                mc.loadSaltFile(saltFile)
            else:
                mc.createSaltFile(saltFile)

            mc.createInternalKey()

        # walletFile = pj(directory, walletFileName)

        if exists(walletFile):
            print('that wallet already exists. aborting.')
            exit()
        else:
            with open(walletFile, 'w') as wf:
                for i in range(numberOfWallets):
                    name = walletNamePrefix + str(i)
                    address, pk = self.generateKeyPair()
                    if walletEncrypted:
                        pk = mc.encryptString(pk)
                    wf.write(','.join([name,address,pk]) + '\n')
    
    def encryptExistingWallet(self, oldWalletFileName, newWalletFileName, saltFile):
        directory = self.walletDir
        if not exists(pj(directory, saltFile)):
            print('need to create salt file first')
            exit()
        elif not exists(pj(directory, oldWalletFileName)):
            print(oldWalletFileName, 'does not exist')
            exit()
        elif exists(pj(directory, newWalletFileName)):
            print(newWalletFileName, 'already exists. aborting')
            exit()
        mc = myCrypt()
        mc.loadSaltFile(pj(directory, saltFile))
        mc.createInternalKey()

        fOld = open(pj(directory, oldWalletFileName), 'r')
        fNew = open(pj(directory, newWalletFileName), 'w')

        for line in fOld:
            nm, pubKey, priKey = line.strip().split(',')
            priKeyEnc = mc.encryptString(priKey)
            fNew.write(','.join([nm, pubKey, priKeyEnc]) + '\n')

        fOld.close()
        fNew.close()
        
                    
