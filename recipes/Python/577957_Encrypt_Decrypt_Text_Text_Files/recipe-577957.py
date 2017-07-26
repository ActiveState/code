"""
@Author = Alex Wallar
"""
from javax.swing import *
from java.lang import *
from java.awt import *
from math import ceil, log
from random import choice, randint

class EncryptionAndDecryption:
    
    getVar = lambda self,searchList, ind: [searchList[i] for i in ind]
    find = lambda self,searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]
    mod = lambda self,n,m: n % m
    
    def set_up_cipher(self): #Use this to change your cipher
        alpha = '\'1234567890qwertyuiop[]asdfghjkl;zxcvbnm,.!@#$%^&*()_+-=-{}:<>|\/QWERTYUIOPASDFGHJKLZXCVBNM ~`?\"\n\t\\'
        cipher = "".join([list(alpha)[randint(0,len(list(alpha))-1)] for i in range(5000)])
        f = open('cipher.txt','r+')
        f.truncate()
        f.close()
        f = open('cipher.txt','r+')
        f.write(cipher)
        f.close()

    def baseExpansion(self,n,c,b):
        i = len(n)
        base10 = sum([pow(c,i-k-1)*n[k] for k in range(i)])
        j = int(ceil(log(base10 + 1,b)))
        baseExpanded = [self.mod(base10//pow(b,j-p),b) for p in range(1,j+1)]
        return baseExpanded
    
    cipherFile = open('cipher.txt')
    cipher = cipherFile.read()
    def wordEncrypt(self,word):
        cipherWord = self.find(self.cipher,list(word))
        keys = [randint(5001,7000), randint(2,5000)]
        encryptedWord = self.baseExpansion(list(map(choice, cipherWord)),keys[0],keys[1])
        encryptedWord.extend(keys)
        return list(map(int,encryptedWord))
        
    def wordDecrypt(self,encryptedList):
        encryptedWord = encryptedList[0:len(encryptedList)-2]
        keys = encryptedList[len(encryptedWord):len(encryptedList)]
        decryptedList = map(int,self.baseExpansion(encryptedWord, keys[1], keys[0]))
        return "".join(self.getVar(self.cipher,decryptedList))
    cipherFile.close()
frame = JFrame('Encryption & Decryption')
frame.setLayout(GridLayout(1, 2))
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)

userChoicePanel = JPanel(GridLayout(4, 1))
inputOutputPanel = JPanel(GridLayout(4, 1))
inputPanel = JPanel(GridLayout(1, 2))
radioButtonEorDPanel = JPanel(GridLayout(1, 2))
radioButtonForWPanel = JPanel(GridLayout(1, 2))

eOrdLabel = JLabel('Encryption or Decryption')
fOrwLabel = JLabel('File or Word')
outputLabel = JLabel('Output:')
inputLabel = JLabel('Please Enter a Word or a Filename:')

inputText = JTextArea(editable=True)
outputText = JTextArea(editable=False)

outputText.setLineWrap(True)
outputText.setWrapStyleWord(True)
areaScrollPane1 = JScrollPane(outputText)
areaScrollPane1.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)

inputText.setLineWrap(True)
inputText.setWrapStyleWord(True)
areaScrollPane2 = JScrollPane(inputText)
areaScrollPane2.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED)

buttonGroupeOrd = ButtonGroup()
buttonGroupfOrw = ButtonGroup()

eRadioButton = JRadioButton('Encrypt')
dRadioButton = JRadioButton('Decrypt')
fRadioButton = JRadioButton('File')
wRadioButton = JRadioButton('Word')

buttonGroupeOrd.add(eRadioButton)
buttonGroupeOrd.add(dRadioButton)
buttonGroupfOrw.add(fRadioButton)
buttonGroupfOrw.add(wRadioButton)

def mainAction(event):
    eAd = EncryptionAndDecryption()
    if inputText.text.lower().rstrip() == 'set up cipher':
        try:
            eAd.set_up_cipher()
            outputText.text = 'The Cipher has been created'
        except:
            outputText.text = 'cipher.txt has not been created'
    else:
        if eRadioButton.isSelected():
            if fRadioButton.isSelected():
                outputText.text = 'Encrypting...'
                try:
                    word = open(inputText.text, 'r+')
                    encryptedWord = eAd.wordEncrypt(word.read())
                    word.close()
                    word = open(inputText.text, 'r+')
                    word.truncate()
                    word.write(str(encryptedWord))
                    word.close()
                    outputText.text = 'The Text File Has Been Encrypted'
                except:
                    outputText.text = 'Please enter valid filename or character'
            elif wRadioButton.isSelected():
                try:
                    outputText.text = 'Encrypting...'
                    encryptedWord = str(eAd.wordEncrypt(inputText.text))
                    outputText.text = encryptedWord
                except:
                    outputText.text = 'You have entered an invalid character'
            else: 
                outputText.text = 'Please Choose File or Word'
        elif dRadioButton.isSelected():
            if fRadioButton.isSelected():
                outputText.text = 'Decrypting...'
                try:
                    word = open(inputText.text, 'r+')
                    decryptedWord = eAd.wordDecrypt(eval(word.read()))
                    word.close()
                    word = open(inputText.text, 'r+')
                    word.truncate()
                    word.write(str(decryptedWord))
                    word.close()
                    outputText.text = 'The Text File Has Been Decrypted'
                except:
                    outputText.text = 'Please enter a valid filename'
            elif wRadioButton.isSelected():
                try:
                    outputText.text = 'Decrypting...'
                    decryptedWord= str(eAd.wordDecrypt(eval(inputText.text)))
                    outputText.text = decryptedWord
                except:
                    outputText.text = 'Please enter the correct format of the Encrypted word'
            else:
                outputText.text = 'Please Choose File or Word'
        else:
            outputText.text = 'Please Choose the Radio Buttons'
                           
goButton = JButton('Go!', actionPerformed=mainAction)

radioButtonEorDPanel.add(eRadioButton)
radioButtonEorDPanel.add(dRadioButton)
radioButtonForWPanel.add(fRadioButton)
radioButtonForWPanel.add(wRadioButton)

inputPanel.add(areaScrollPane2)
inputPanel.add(goButton)

inputOutputPanel.add(inputLabel)
inputOutputPanel.add(inputPanel)
inputOutputPanel.add(outputLabel)
inputOutputPanel.add(areaScrollPane1)

userChoicePanel.add(eOrdLabel)
userChoicePanel.add(radioButtonEorDPanel)
userChoicePanel.add(fOrwLabel)
userChoicePanel.add(radioButtonForWPanel)

frame.add(userChoicePanel)
frame.add(inputOutputPanel)

frame.show()
