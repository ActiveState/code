#####################################################################
# program name: guess.py
# auther: max baseman
# email: dos.fool@gmail.com
# date: 5/01/07
# short description: 
# this is a program that has two features
# one that randomly picks numbers till it gets yours
# and one that picks the most effective way till it gets your number
#####################################################################

from random import randrange as random
print "welcome to a number guessing program"
print
print "enter 1 for random "
print "or"
print "enter 2 for efficient"
print
guesstype=input(" >")
if guesstype == 1:
    number=input("pick a number >")
    numrange=input("pick a range >")+1
    guessed=[0]
    guess=random(numrange)
    if guess==0:
        guess=random(numrange)
    print guess
    guessed.append(guess)
    guesses=1
    while guess!=number:
        guessed.append(guess)
        guesses=guesses+1
        guess=random(numrange)
        if guess in guessed:
            while guess in guessed:
                guess=random(numrange)
        print guess
    print"i got the number",number,"in",guesses,"guesses, out of a range of",numrange-1
elif guesstype == 2:
    number=input("pick a number >")
    numrange=input("pick a range >")+1
    guess=numrange/2
    print guess
    guesses=1
    min=0
    max=numrange
    while guess!=number:
        if guess < number:
            min=guess
        else:
            max=guess
        guess = (min+max) /2
        guesses= guesses +1
        print guess
    print "i got the number",number,"in",guesses,"guesses, out of a range of",numrange-1
print

    
    
        
    
    
                
                
