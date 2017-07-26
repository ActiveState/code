# the 5th sharif acm contest: number 2:SMS lock decrypt program

"""
THE PROBLEM:

This year, ACM scientific committee members use emails to discuss 
about the problems and edit the selected ones. They know that email is 
not a secure way of communication, especially on such an important 
topic. So they transfer password-protected compressed file among 
themselves. In order to send the passwords, they use SMS. To increase 
the security level, the encrypted passwords are sent by SMS. To do this, a 
multi-tap SMS typing method is used. 
Multi-tap is currently the most common text input method for mobile 
phones. With this approach, the user presses each key one or more times 
to obtain the wanted characters. For example, the key 2 is pressed once to 
get character A, twice for B, and three times for C. 
The encryption algorithm that is used is quite simple: to encrypt the  ith
 
character of the password, the key used to obtain that character is tapped i 
more times. For if the 4th
 character of password is U, the key 8 is tapped 6 
times, getting the character V. Note that to make the problem simple, we 
have assumed that the keypad does not generate digits.  
 
 
The scientific committee needs a program to decrypt the received 
passwords. They are too busy to write this program and have asked you to help!  Write a program to get a correct 
encrypted text and print the original password.

INPUT                      OUTPUT
----------------------------------
BACE                       ABCD
GgaudQNS                   IhateSMS

__to imagine better use your phone keyboard
__there is two function: encrypt and decrypt the answer of problem is decrypt and encrypt do reversed decrypt.  

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

code explanation:
__r: real number ,real character position in cellphone keyboard ,for example "E" is 1.
__v: virtual number (encrypted)
__n: character number in string
__notice that in python lists start with 0,
__for example to encrypt "ABCD", number of "A" in string is 0
"B" is 1,"C" is 2 and "D" is 1("DEF").
__to encrypt "A":r=0 , n:1 then v=r+n ,v=1 ,1 in keyboard is "B".
__to convert "B":r=1 , n=2 then v=r+n ,v=3 ,4 we have not 4 in keybord(ABC IN KEY "2")
but we cvan use "%" operator so we have 3%3=0 then we have "A". 3 is length of("ABC"),
see your cell phone if you not understand.
__to encrypt "C":r=2 , n=3 then v=r+n , 5%3=2 and 2 is "C" itself.
__to encrypt "D":r=0 , n=4 then v=4   , 4%3=1 and 1 is "E" .
__so we convert "ABCD" to "BACE". 

"""

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

def det(c,num):
    """ c:character and num :r or real number, takes a character
        and a number ,then returns character that belongs to c's list(given character ' lsit) using num
        for example we give it "a" and 2 then  returns c """
    flag=0
    l2=['a','b','c']
    gl2=['A','B','C']
    l3=['d','e','f']
    gl3=['D','E','F']
    l4=['g','h','i']
    gl4=['G','H','I']
    l5=['j','k','l']
    gl5=['J','K','L']
    l6=['m','n','o']
    gl6=['M','N','O']
    l7=['p','q','r','s']
    gl7=['P','Q','R','S']
    l8=['t','u','v']
    gl8=['T','U','V']
    l9=['w','x','y','z']
    gl9=['W','X','Y','Z']
    all=[l2,l3,l4,l5,l6,l7,l8,l9,gl2,gl3,gl4,gl5,gl6,gl7,gl8,gl9]
    retl=[]    # return list


    for i in all:
        if c in i:
            retl=i
            
    return retl[num]
# ------------------------------------
def num(list,c):
    " return character number in a given list "
    if ord(c)>65 and ord(c)<91:
        c=chr(ord(c)+32)
    for i in range(len(list)):
        if list[i]==c:
            return i
    return False
# ------------------------------------

# ------------------------------------
def what(c):
    " determines that the given charater (c) belongs to witch list "
    flag=0
    l2=['a','b','c']
    gl2=['A','B','C']
    l3=['d','e','f']
    gl3=['D','E','F']
    l4=['g','h','i']
    gl4=['G','H','I']
    l5=['j','k','l']
    gl5=['J','K','L']
    l6=['m','n','o']
    gl6=['M','N','O']
    l7=['p','q','r','s']
    gl7=['P','Q','R','S']
    l8=['t','u','v']
    gl8=['T','U','V']
    l9=['w','x','y','z']
    gl9=['W','X','Y','Z']
    all=[l2,l3,l4,l5,l6,l7,l8,l9,gl2,gl3,gl4,gl5,gl6,gl7,gl8,gl9]
    retl=[]    # return list
    
    if ord(c)<91 and ord(c)>64:        # in all case we make characters in small case
        flag=1
        c=chr(ord(c)+32)

    for i in all:
        if c in i:
            return i
# --------------------------------------------------
####################################################
####              # ENCRYPT Fun()               ####
####################################################

def encrypt(string):
    list=[]
    retstr=''
    snum=1  # character number in string
    r=int()   # real number usin num
    v=int()    # virtual number

    for chr in string:
        if chr==' ' or type(i)==type(2): # if you put number it pirnts space. 
            retstr+=' '
            continue
        list=what(chr)
        r=num(list,chr)   # real number
        v=snum+r          # virtual number
        v=v%len(list)
        retstr+=det(chr,v)
        snum+=1

    return retstr
# --------------------------------------------------------------
################################################################
#####                     DECRYPT fun()                    #####
################################################################
def decrypt(string):
    r=0
    v=0    # number in list usin num() , virtual
    n=0    # number in string; num() can be used - * virtual
    secchr=''   # for returning
    list=[]
    count=0

    for i in string:
        if i==" " or type(i)==type(2): # if you put number it pirnts space. 
            secchr+=' '
            continue
        list=what(i)
        v=num(list,i)
        n=count+1
        r=v-n  # real number
        r=r%len(list)
        secchr+=det(i,r)
        count+=1
    return secchr
        



# RUNNING:
# ---------------------------------------------x        
if __name__=="__main__":
    a=raw_input('decrypt or encrypt ?( d/e) ')
    word=raw_input('enter word ')
    if a=='d':
        print decrypt(word)
    elif a=='e':
        print encrypt(word)
