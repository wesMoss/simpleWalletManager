import os
from walletManager import walletManager


cwd = os.getcwd()
pj = os.path.join
exists = os.path.exists


testDir = pj(cwd, 'testWallets')
if not exists(testDir):
    os.mkdir(testDir)

#new walletManager object
wm = walletManager(testDir)

#generate a key pair
address, privateKey = wm.generateKeyPair()
print('address, private key:', address, privateKey)


#create unencrypted wallet file
saltFileName = '' #no salt file means cleartext wallet
walletNamePrefix = 'myWallet-'
unencWallet = 'walletsUnencrypted.txt'
wm.createNewWalletsAutoGenerate(unencWallet, 
                                saltFileName='', 
                                numberOfWallets=5, 
                                walletNamePrefix='myWallet-')

#read wallet
wm.openWalletFile(unencWallet, saltFileName)
#display wallet info
for name in wm.walletsInfo:
    print(name, wm.walletsInfo[name])



#salt file will be used for encryption
saltFileName = 'saltFile2.txt'
wm.createSaltFile(saltFileName)

#create new encryptedWallet
encWallet = 'walletsEncrypted.txt'
#window will pop up asking for password
wm.createNewWalletsAutoGenerate(encWallet, 
                                saltFileName=saltFileName, 
                                numberOfWallets=5, 
                                walletNamePrefix='myWalletEncrypted-')

#encrypt first wallet
encWallet = 'walletsEncrypted2.txt'
#window will pop up asking for password
wm.encryptExistingWallet(unencWallet, encWallet, saltFileName)


#read encrypted wallet
wm.openWalletFile(encWallet, saltFileName)
#display wallet info
for name in wm.walletsInfo:
    pk = wm.getPrivateKey(name)
    print(name, wm.walletsInfo[name])
    print(pk)

#add new address to encrypted wallet by hand via gui
wm.addWalletInfoToWalletFileManual(encWallet, saltFileName)





