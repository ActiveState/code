# just a simple game of poker dice, using 5 dice - with the 
# computer  throwing for you - and then  you choose which 
# dice to keep or reuse for the next throw
import os
def clear():
    os.system("clear")
clear()
print
print "    Poker dice game  "

px = 2
while px == 2:
    print
    print "    The compuuter will help you throw your 5 dice  "
    print

    rand = range(1,7)
    import random
    dice = range(5)

    y =0
    while y < 5:
       y = y + 1
       dice[y-1] = random.choice(rand)

    print " The throw gives the following result .. ",  dice
    
    for i in range(len(dice)):
        print " dice position No.",i + 1,"\t"," .... throws ..",dice[i]

    print
    howmany = input('How many dice do you want to\
 throw again\nto make full house, or five of a kind etc.....>>>>  ')
 
    print
    print "Input the dice position number to remove the dice\
,\nand REMEMBER to press enter each time\n(except when you choose\
 a complete re-throw)"
    print
    tt = 0
    while tt < howmany:
       tt = tt + 1
       if howmany == 5:
          break
       yy  = input (' ...>>> ')
       if yy == 1 and tt == 1:
           del dice[0]
       if yy == 2 and tt == 1:
           del dice[1]
       if yy == 2 and tt == 2:
           del dice[0]
       if yy == 3 and tt == 1:
           del dice[2]
       if yy == 3 and tt == 2:
           del dice[1]
       if yy == 3 and tt == 3:
           del dice[0] 
       if yy == 4 and tt == 1:
           del dice[3]
       if yy == 4 and tt == 2:
          del dice[2]
       if yy == 4 and tt ==3:
          del dice[1]
       if yy == 4 and tt == 4:
         del dice[0]
       if yy == 5 and tt == 1:
         del dice[4]
       if yy == 5 and tt == 2:
         del dice[3]
       if yy == 5 and tt == 3:
         del dice[2]
       if yy == 5 and tt == 4:
          del dice[1]
       if yy == 5 and tt == 5:
          del dice[0]
    
    if howmany < 5:
       print "your first throw (i.e dice kept) ... ",dice
    if howmany == 5:
       print "dice kept = none"
    dice2 = range(howmany)
    y =0
    while y < howmany:
       y = y + 1
       dice2[y-1] = random.choice(rand)

    uu = 0
    while uu < howmany:
       uu = uu + 1
       fff = dice2[uu-1]
       dice.insert(0,fff)
    print
    if  howmany <  5:
        print "The new throw(s) give you ... ",dice2
    print
    if howmany < 5:
        for i in range(len(dice)):
            print " Dice position No.",i + 1,"(b)"," ...... ",dice[i]

    print
    if howmany == 5:
        for i in range(len(dice2)):
            print " Dice position No.",i + 1,"(b)"," ...... ",dice2[i]
    print

    again = raw_input("Do you want to play poker dice\
 again,\nenter y for yes and n for no ...  ")
    if again == 'y':
      px = 2
    if again == 'n':
      px = 0
print
print "finish"
