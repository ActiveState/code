import sys, os, time
def binaryToDigital():
    os.system('cls')
    while True:
        print "To go back to the main menu type 'e' and press enter"
        print
        print """Binary numbers consist of only '1's and '0's 
        """
        binary = raw_input('Type in the binary number: ')
        if binary == "e":
            mainmenu()
        else:
            binarylist = list(binary)
            no = len(binarylist)
            no = no -1
            diginum = 0
            i = 0
            while no > -1:
                if binarylist[no] == '1':
                    kj = 2**i
                    diginum = diginum + kj
                no = no -1
                i = i +1 
            print diginum
            raw_input()

def digitalToBinary():
    os.system('cls')
    try:
        while True:    
            print "To go back to the main menu type 'e' and press enter" 
            print
            number = raw_input('Type in the digital number: ')
            if number == "e":
                mainmenu()
            else:
                number = int(number)
                aaa = str(number)
                i = 0
                numlist = []
                while number != 0:
                    numlist.append(number)
                    number = number/2 
                    i = i + 1
                binarynum = []
                i = i-1
                while i !=-1:
                    bd = str(numlist[i])
                    bdl = list(bd)
                    bdn = len(bdl)
                    bdn = bdn - 1
                    bx = bdl[bdn]
                    if bx == '0' or bx == '2' or bx == '4' or bx == '6' or bx == '8':
                        binarynum.append('0')
                    if bx == '1' or bx == '3' or bx == '5' or bx == '7' or bx == '9':
                        binarynum.append('1')
                    i = i - 1
                print ''.join(binarynum)
                raw_input()
    except ValueError:
        print "The input should only numbers"
        digitalToBinary()
        raw_input()
def credit():
    os.system('cls')
    text = """###########################
Author: phinix bss
Date  : 04/06/2006
Vision: Binary-converter 1.0
###########################
    """
    for character in text:
        sys.stdout.write(character);sys.stdout.flush(),time.sleep(.03),
    raw_input()

def mainmenu():
    while True:
        os.system('cls')
        menu = """What du you want to do?

1) Convert digital to binary
2) Convert binary to digital
3) Credits
4) Exit

pick choice [1-4] : """
        choice = raw_input(menu)
        if choice == "1":
            digitalToBinary()
        if choice == "2":
            binaryToDigital()
        if choice == "3":
            credit()
        if choice == "4":
            sys(exit)
mainmenu()
