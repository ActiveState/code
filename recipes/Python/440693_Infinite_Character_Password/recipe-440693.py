from random import choice as randomChoice

global passData
global password

passData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '=',
            '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']

def newPass():
    while True:
        try:
            passwdNum = int(raw_input("Enter max number of characters: "))
        except TypeError:
            print "Please enter a digit."
            continue
        break        
    gen(passwdNum)

def gen(number):
    password = []
    number = int(number)
    count = 0
    print "\nGenerating password..."
    while count != number:
        password.append(randomChoice(passData))
        count += 1
    x = 0
    p = ''
    while x != len(password):
        p = p + str(password[x])
        x += 1    
    print "Password generated.",
    print "Here's your %s character password. Note that there may be spaces: %s" % (len(password), p)

newPass()
