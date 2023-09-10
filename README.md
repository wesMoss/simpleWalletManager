# simpleWalletManager

A Python library to manage Ethereum addresses and their respective private keys. With this library, you can store Ethereum wallet details locally, with an option for encryption.

## Features

- Generate key pairs
- Create and store multiple Ethereum wallets, either with or without encryption
- Encrypt existing wallets
- Open existing wallets for use in your bot application

## Prerequisites

Make sure you have Python installed, preferably version 3.6 or higher.
1. Install python dependencies
    ```bash
    pip3 install easygui eth_account cryptography
    ```

## Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/wesMoss/simpleWalletManager.git
    ```

2. Navigate to the project directory:
    ```bash
    cd walletManager
    ```

## Usage 

### Create a new walletManager instance:

```python
from walletManager import walletManager

wm = walletManager(walletDir="path_to_directory")
```

### generate a key pair
```python
address, privateKey = wm.generateKeyPair()
```


### create unencrypted wallet file
```python
saltFileName = '' #no salt file means cleartext wallet
walletNamePrefix = 'myWallet-'
unencWallet = 'walletsUnencrypted.txt'
wm.createNewWalletsAutoGenerate(unencWallet, 
                                saltFileName='', 
                                numberOfWallets=5, 
                                walletNamePrefix='myWallet-')
```

### read wallet
```python
wm.openWalletFile(unencWallet, saltFileName)
#display wallet info
for name in wm.walletsInfo:
    print(name, wm.walletsInfo[name])
```



### Generate a "salt" file
```python
saltFileName = 'saltFile2.txt'
wm.createSaltFile(saltFileName)
```

### create new encryptedWallet, using salt file, along with a password
```python
encWallet = 'walletsEncrypted.txt'
#window will pop up asking for password
wm.createNewWalletsAutoGenerate(encWallet, 
                                saltFileName=saltFileName, 
                                numberOfWallets=5, 
                                walletNamePrefix='myWalletEncrypted-')
```

### encrypt the first, unencrypted wallet
```python
encWallet = 'walletsEncrypted2.txt'
#window will pop up asking for password
wm.encryptExistingWallet(unencWallet, encWallet, saltFileName)
```


### read encrypted wallet
```python
wm.openWalletFile(encWallet, saltFileName)
#display wallet info
for name in wm.walletsInfo:
    pk = wm.getPrivateKey(name)
    print(name, wm.walletsInfo[name])
    print(pk)
```

### add new address to encrypted wallet by hand via gui
```python
wm.addWalletInfoToWalletFileManual(encWallet, saltFileName)
```

## Caution

This library is unaudited. Please use at your own risk.

## Contributing

I'd be very interested in learning about any bugs or security holes in this library. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT



