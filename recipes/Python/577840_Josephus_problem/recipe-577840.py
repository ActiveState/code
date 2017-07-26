#!/usr/bin/env python

#let's speak about cladiators and the survivor (Josephus)

import sys
from math import log

CLDTRS_NUMBER = 0

last2first = lambda L : L[-1::] + L[0:len(L) -1]


def wholives(n):
## ---We search Within lowest-highest power of 2 that n Gladiators resides---
## wholives Function assumes that we have assigned each Gladiator a number in ascending order
## (in a way that Gladiators are ordered as they --have,need or must -- to. The numbers just follow their order)
## wholives is a FAST FUNCTION WITH CONSTANT TIME COMPLEXITY
## We calculate the log2 of the number of Gladiators if it is integer then we subtract one from the number raised in
## powers of 2 then we subtract the number of Gladiators from the base power and finally we subtract it from the number of
## Gladiators. If it the log2 is not integer we take the next exponent (successor) as Base
## The key here is that at every increment of exponent of power of 2 (minus 1) we can calculate all the previous Gladiators down to
## the previous exponent( minus 1) just by subtracting the nearest higher power of 2 (minus 1) and from Gladiators n and then
## subtracting the result from the Gladiators n itself.
## in order to select efficiently the correct nearest higher exponent we simply calculate the log2 of n Gladiators
## if it is integer we are in (we can use it as our Base exponent)
## it it is not then it means we need to take the next higher exponent for our Base exponent
## we are not interesting into any result of log2 of n Gladiators that is not integer since the subtractions
## between the limits of the lower power and higher power can give us the result
    
    #there are two base cases
    # if there are two Gladiators the first survives because he has the Sword
    # if there is only one Gladiator ..he is already the Survivor...
    if n == 1:
        return 1
    if n == 2:
        return 1

    LogN = log(n,2)

    if not LogN.is_integer():
        BaseExpo = int(LogN) + 1
        BasePower = int(pow(2,BaseExpo)) - 1
        Sub = BasePower - n
        Res = n - Sub
        return Res
    else:
        #Here we need to restart counting
        #eg 7 lives 7 (2^3 -1) ,15 lives 15 (2^4 -1) ,31 lives 31 (2^5 -1) ,63 lives 63 (2^6 -1)\
        # 127 lives 127 (2^7 -1 ) so we can just return 1 to restart at 8 , 16 , 32, 64, 128 respectively
        # and so on and so forth...
        #BaseExpo = int(LogN)
        #BasePower = int(pow(2,BaseExpo)) - 1
        #Sub = BasePower - n
        #Res = n - Sub
        #return Res
        return 1



def isNotEven(x):
    if not x % 2:
        return False
    else:
        return True


def PrepareCladiators(NUMBER):
    cladiators = tuple(xrange(1,NUMBER + 1))
    return cladiators


def Survivor(cladiators):
    
    if len(cladiators) < 2:
        raise Exception ,"\n\n***** Cladiators must be at least 2!!! ***** \n"
##
##
## print"\nCeasar says:\n\tLET THE DEATH MATCH BEGIN!!!\
## \n\nThey started kiling each other... \nEach one kills the next one\
## \nand passes the Sword to the next one alive.. \
## \nthere are all",len(cladiators)," still alive and here they are \n" ,cladiators
    
    FirstClads = len(cladiators)
    Clads = cladiators
    deathcycle =0
    
    while len(Clads) > 1 :
        if isNotEven(len(Clads)):
            deathcycle += 1
            Clads = Clads[::2]
            Clads = last2first(Clads)
##
## print "\n",len(Clads), "left alive after the",deathcycle,"death cycle and "\
## ,FirstClads - len(Clads)," have died till know"
## print "\nThese are the live ones\n",Clads
##
        else:
            deathcycle += 1
            Clads = Clads[::2]
##
## print "\n",len(Clads), "left alive after the",deathcycle,"death cycle and "\
## ,FirstClads - len(Clads)," have died till know"
## if len(Clads) > 1 :
## print "\nThese are the live ones\n",Clads
## else :
## print "\n**** The last Survivor **** \nis:\n***\n\tCladiator",Clads[0]\
## ,"\n\n*********************************"

    return Clads[0]
            
        


if __name__ == "__main__":


    try :
        CLDTRS_NUMBER = int(sys.argv[1])
        
## print "\n\t**** Welcome to the Deadly Arena Survivor ****\n"
## print "\n",CLDTRS_NUMBER," Cladiators will fight and \n",CLDTRS_NUMBER -1 ," Cladiators are going to die ...\n"
## print "\tONLY ONE SHALL SURVIVE...\n"
## print "\tBUT who???\n"
## print " ohhh , HERE THEY ARE .. \n"
        
        cladiators = PrepareCladiators(CLDTRS_NUMBER)
        
## print cladiators, "\n\n!!! HAIL Ceasar !!! \nthey say loudly..."
        
        print CLDTRS_NUMBER,Survivor(cladiators)

    except (IndexError ,ValueError ):
        
        print "Please place one integer value as arguement\n"
