from random import randint,choice
from math import ceil,log

getVar = lambda searchList, ind: [searchList[i] for i in ind]
find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]
mod = lambda n,m: n % m

def set_up_cipher(): #Use this to change your cipher
    alpha = '1234567890qwertyuiop[]asdfghjkl;zxcvbnm,.!@#$%^&*()_+-=-{}:<>|QWERTYUIOPASDFGHJKLZXCVBNM ~`?°'
    cipher = "".join([list(alpha)[randint(0,len(list(alpha))-1)] for i in range(5000)])
    f = open('cipher.txt','r+')
    f.truncate()
    f = open('cipher.txt','r+')
    f.write(cipher)

def baseExpansion(n,c,b):
    i = len(n)
    base10 = sum([pow(c,i-k-1)*n[k] for k in range(i)])
    j = int(ceil(log(base10 + 1,b)))
    baseExpanded = [mod(base10//pow(b,j-p),b) for p in range(1,j+1)]
    return baseExpanded

cipher = open('cipher.txt').read()+'\n'
def wordEncrypt(word):
    cipherWord = find(cipher,list(word))
    keys = [randint(5001,7000), randint(2,5000)]
    encryptedWord = baseExpansion(list(map(choice, cipherWord)),keys[0],keys[1])
    encryptedWord.extend(keys)
    return list(map(int,encryptedWord))
    
def wordDecrypt(encryptedList):
    encryptedWord = encryptedList[0:len(encryptedList)-2]
    keys = encryptedList[len(encryptedWord):len(encryptedList)]
    decryptedList = map(int,baseExpansion(encryptedWord, keys[1], keys[0]))
    return "".join(getVar(cipher,decryptedList))

def mainEandD(): #Interactive 
    print('Please Enter e for Encryption or d for Decryption')
    print(' ')
    counter = True
    counter2 = True
    while counter:
        while counter2:
            func = input('Encrypt or Decrypt: ')
            print(' ')
            if func.lower() == 'e':
                print('Would You Like to Encrypt a Word or a Text File?')
                print(' ')
                while True:
                    fOrw = input('F/W: ')
                    print(' ')
                    if fOrw.lower().rstrip() == 'w':
                        word = input('Enter Word: ')
                        print(' ')
                        print('Encrypting...')
                        print(' ')
                        print('The Encrypted Word is: {}'.format(wordEncrypt(word)))
                        print(' ')
                        counter2 = False
                        break
                    elif fOrw.lower().rstrip() == 'f':
                        while True:
                            try:
                                wordInput = input('Enter Filename: ')
                                print(' ')
                                print('Encrypting...')
                                print(' ')
                                word = open(wordInput, 'r+')
                                encryptedWord = wordEncrypt(word.read())
                                word.close()
                                word = open(wordInput, 'r+')
                                word.truncate()
                                word.write(str(encryptedWord))
                                word.close()
                                print('The Text File Has Been Encrypted')
                                print(' ')
                                counter2 = False
                                break
                            except:
                                print(' ')
                                print('Enter a Valid Filename or Type')
                                print(' ')
                        break
                    else:
                        print('Please enter f for File or w for Word')
                        print(' ')
            elif func.lower() == 'd':
                print('Would You Like to Decrypt a Word or Text File?')
                print(' ')
                while True:
                    fOrw = input('F/W: ')
                    print(' ')
                    if fOrw.lower().rstrip() == 'w':
                        while True:
                            try:
                                encryptedWord = eval(input('Enter Encrypted Word: ').rstrip())
                                print(' ')
                                print('Decrypting...')
                                print(' ')
                                print('The Decrypted Word is: {}'.format(wordDecrypt(encryptedWord)))
                                print(' ')
                                counter2 = False
                                break
                            except:
                                print(' ')
                                print('You did not enter a the correct type')
                                print(' ')
                        break
                    elif fOrw.lower().rstrip() == 'f':
                        while True:
                            try:
                                wordInput = input('Enter Filename: ')
                                print(' ')
                                print('Decrypting...')
                                print(' ')
                                word = open(wordInput, 'r+')
                                decryptedWord = wordDecrypt(eval(word.read()))
                                word.close()
                                word = open(wordInput, 'r+')
                                word.truncate()
                                word.write(str(decryptedWord))
                                word.close()
                                print('The Text File Has Been Decrypted')
                                print(' ')
                                counter2 = False
                                break
                            except:
                                print(' ')
                                print('You did not enter a the correct type or Filename')
                                print(' ')
                        break
                    else:
                        print('Please enter f for File or w for Word')
                        print(' ')
            else:
                print('Please Enter e for Encryption and d for Decryption')
                print(' ')
        print('Would you like to Encrypt or Decrypt another word or file?')
        print(' ')
        while True:
            tryAgain = input('Y/N: ')
            print(' ')
            if tryAgain.lower().rstrip() == 'n':
                print('Thank You!')
                print(' ')
                counter = False
                break
            elif tryAgain.lower().rstrip() == 'y':
                counter2 = True
                break
            else:
                print('Please Enter Either Y for Yes or N for No')
                print(' ')
                
#mainEandD()
