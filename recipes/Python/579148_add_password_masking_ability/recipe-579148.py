# created by https://github.com/kingmak

import sys, msvcrt

def getpass(prompt = 'Password: ', hideChar = ' '):

    count = 0
    password = ''
    
    for char in prompt:
        msvcrt.putch(char)# cuz password, be trouble
        
    while True:
        char = msvcrt.getch()
        
        if char == '\r' or char == '\n':
            break
        
        if char == '\003':
            raise KeyboardInterrupt # ctrl + c

        if char == '\b':
            count -= 1
            password = password[:-1]

            if count >= 0:
                msvcrt.putch('\b')
                msvcrt.putch(' ')
                msvcrt.putch('\b')
            
        else:
            if count < 0:
                count = 0
                
            count += 1
            password += char
            msvcrt.putch(hideChar)
            
    msvcrt.putch('\r')
    msvcrt.putch('\n')
    
    return "'%s'" % password if password != '' else "''"

# password = getpass('Password: ', '*')
password = getpass(hideChar = '*')
raw_input('pass = ' + password)
