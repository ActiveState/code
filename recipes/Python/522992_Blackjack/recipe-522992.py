#Blackjack by Mike McGowan
#It's Monday, June 25, 2007 as of now, but I'm pretty sure I finished this
#a week or two ago. I cleaned it up yesterday.

import random as r
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]*4
dealer = []
player = []
c = 'y'

#Clear works only if you run it from command line
def clear():
    import os
    if os.name == 'nt':
        os.system('CLS') #Pass CLS to cmd
    if os.name == 'posix':
        os.system('clear') #Pass clear to terminal
    
def showHand():
    hand = 0
    for i in player: hand += i #Tally up the total
    print "The dealer is showing a %d" % dealer[0]
    print "Your hand totals: %d (%s)" % (hand, player)

#Gives player and dealer their cards
def setup():
    for i in range(2):
        dealDealer = deck[r.randint(1, len(deck)-1)]
        dealPlayer = deck[r.randint(1, len(deck)-1)]
        dealer.append(dealDealer)
        player.append(dealPlayer)
        deck.pop(dealDealer)
        deck.pop(dealPlayer)
setup()
while c != 'q':
    showHand()
    c = raw_input("[H]it [S]tand [Q]uit: ").lower()
    clear()
    if c == 'h':
        dealPlayer = deck[r.randint(1, len(deck)-1)]
        player.append(dealPlayer)
        deck.pop(dealPlayer)
        hand = 0
        for i in dealer: hand += i
        if not hand > 17:   #Dealer strategy.
            dealDealer = deck[r.randint(1, len(deck)-1)]
            dealer.append(dealDealer)
            deck.pop(dealDealer)
        hand = 0
        for i in player: hand += i
        if hand > 21:
            print "BUST!"
            player = []     #Clear player hand
            dealer = []     #Clear dealer's hand
            setup()         #Run the setup again
        hand = 0
        for i in dealer: hand +=i
        if hand > 21:
            print "Dealer Busts!"
            player = []
            dealer = []
            setup()
    elif c == 's':
        dHand = 0           #Dealer's hand total
        pHand = 0           #Player's hand total
        for i in dealer: dHand += i
        for i in player: pHand += i
        if pHand > dHand:
            print "FTW!"    #If playerHand (pHand) is greater than dealerHand (dHand) you win...
            dealer = []
            player = []
            setup()
        else:
            print "FTL!"    #...otherwise you loose.
            dealer = []
            player = []
            setup()
    else:
        if c == 'q':
            gb = raw_input("Toodles. [Hit Enter]")
        else:
            print "Invalid choice."
