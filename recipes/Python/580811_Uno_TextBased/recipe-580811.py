import os
import sys
import random
import math
import time

class BadInputError(Exception):
    pass

class Player():

    def __init__(self, name):
        self.id = None
        self.name = name
        self.type = 'Human'
        self.hand = Hand()
        self.legalCards = []
        self.wildCards = []
        self.valueChangeCards = []
        self.zeroCards = []
        self.canSkip = False
        self.canReverse = False
        self.canDrawTwo = False
        self.canDrawFour = False
        self.canValueChange = False
        self.drew = False
        self.scrollMax = 0
        self.points = 0
        self.forceDraw = 0

    def addCard(self, card):
        self.drew = True
        if self.forceDraw > 0:
            self.forceDraw -= 1
            self.drew = False
        self.hand.addCard(card)
        
    def beginTurn(self):
        self.drew = False
        
    def didDraw(self):
        return self.drew
        
    def getLegalCards(self, color, value, zeroChange=False):
        self.canSkip = False
        self.canReverse = False
        self.canDrawTwo = False
        self.canDrawFour = False
        self.canValueChange = False
        self.canZeroChange = False
        self.legalCards = []
        self.wildCards = []
        self.valueChangeCards = []
        self.zeroCards = []
        plusFours = []
        for card in self.hand:
            if card.isWild():
                if card.getValue() == '+4':
                    plusFours.append(card)
                else:
                    self.wildCards.append(card)
            elif zeroChange and card.isZero():
                self.canZero = True
                self.zeroCards.append(card)
            elif card.getColor() == color or card.getValue() == value:
                if card.getColor() != color:
                    self.canValueChange = True
                    self.valueChangeCards.append(card)
                if card.getValue() == "+2":
                    self.canDrawTwo = True
                elif card.getValue() == 'R':
                    self.canReverse = True
                elif card.getValue() == 'X':
                    self.canSkip = True
                self.legalCards.append(card)
        if len(self.legalCards) == 0 and len(plusFours) > 0:
            self.canDrawFour = True
            self.wildCards += plusFours
                
    def getValidCards(self):
        return self.legalCards
    
    def getAllValidCards(self):
        return self.legalCards + self.wildCards + self.zeroCards
                
    def hasLegalCard(self):
        return len(self.legalCards) > 0
        
    def addPoints(self, amount):
        if (self.points + amount) <= 999999999999999999999:
            self.points += amount
        
    def removeCard(self, index):
        return self.hand.removeCard(index)
    
    def assignID(self, identity):
        self.id = identity

    def getName(self):
        return self.name

    def getID(self):
        return self.id
    
    def getPoints(self):
        return self.points

    def getType(self):
        return self.type

    def getCardNum(self):
        return len(self.hand)

    def getHand(self, scrollNum=0, hide=False):
        return self.hand.show(scrollNum, hide)
    
    def getForceDraws(self):
        return self.forceDraw
    
    def addForceDraw(self, num):
        self.forceDraw += num
    
    def decreaseForceDraw(self):
        self.forceDraw -= 1
        
    def removeForceDraw(self):
        self.forceDraw = 0

    def checkCard(self, index):
        return self.hand.getCard(int(index))
    
    def discardHand(self):
        self.hand.discard()
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return '({},{})'.format(self.name, self.points)

class Hand():
    ''''deck' (Deck) : Card's Color (rgby)
       'numberOfCards' (int) : Card's Value (0-9, R, X, W, +2, +4)'''

    def __init__(self, deck=None,numberOfCards=0):
        self.hand = []
        if deck != None:
            self.draw(deck,numberOfCards)

    def __iter__(self):
        return iter(self.hand)

    def __len__(self):
        return len(self.hand)

    def __getitem__(self, item):
        try:
            return self.hand[item]
        except:
            return ''

    def addCard(self, card):
        self.hand.append(card) 
        
    def removeCard(self, index):
        index = int(index)
        if (0 <= index < len(self)):
            return self.hand.pop(index)      

    def discard(self):
        self.hand = []

    def show(self, scrollNum=0, hide=False):
        if scrollNum == -1:
            scrollNum = 0
        output = ''
        num = 0
        header, footer, upper, lower = '', '', '', ''
        header +=   ('\033[97m\u2666--\u2666\033[0m ')
        upper +=    ('\033[97m|<-|\033[0m ')
        lower +=    ('\033[97m|<-|\033[0m ')
        footer +=   ('\033[97m\u2666--\u2666\033[0m ')
        for i in range(10):
            indexNum = i+(10*scrollNum)
            if indexNum < len(self):
                header += (self[indexNum].getRow(0,hide)+' ')
                upper += (self[indexNum].getRow(1,hide)+' ')
                lower += (self[indexNum].getRow(2,hide)+' ')
                footer += (self[indexNum].getRow(3,hide)+' ')
                num += 1
        for j in range(10-num):
            j #unused
            header += ('     ')
            footer += ('     ')
            upper += ('     ')
            lower += ('     ')
        header +=   ('\033[97m\u2666--\u2666\033[0m ')
        upper +=    ('\033[97m|->|\033[0m ')
        lower +=    ('\033[97m|->|\033[0m ')
        footer +=   ('\033[97m\u2666--\u2666\033[0m ')
        output += ('  '+header+'\n  '+upper+'\n  '+lower+'\n  '+footer+'\n\033[97m|-(<)--')
        for k in range(num):
            output += '({})'.format(k)
            output += '--'
        for l in range(10-num):
            l #unused
            output += '-----'
        output += '(>)--|\033[0m\n'
        return output

    def getCard(self, index):
        return self.hand[index]
    
    def indexCard(self, card):
        return self.hand.index(card)

class GameSettings():
    
    playerIdentities = ('play1','play2','play3','play4')
    computerNames = ('Watson','SkyNet','Hal','Metal Gear')
    
    def __init__(self):
        self.playerStaging = []                  #    Where Player Objs Are Stored Before Game Starts
        self.players = {}                        #    ID : Player Obj
        self.numPlayers = 0
        self.useColor = True 
        self.displayEffects = True
        self.hideComputerHands = True
        self.zeroChange = False
        self.computerSimulation = False
        self.mainMenuError = ''
        self.computerSpeed = 'normal'
        
    def canAddPlayer(self):
        return (self.numPlayers < 4)
    
    def canRemovePlayer(self):
        return (self.numPlayers > 0)
    
    def canBegin(self):
        return (self.numPlayers > 1)
        
    def addPlayer(self, player):
        self.playerStaging.append(player)
        self.numPlayers += 1
        
    def removePlayer(self, number):
        number -= 1
        del self.playerStaging[number]
        self.numPlayers -= 1
        
    def clearStaging(self):
        self.numPlayers = 0
        self.playerStaging = []
        
    def finalizePlayers(self):
        self.players.clear()
        identity = 0
        for player in self.playerStaging:
            playerID = self.playerIdentities[identity]
            player.assignID(playerID)
            self.players[playerID] = player
            identity += 1
        
    def getPlayerNum(self):
        return self.numPlayers
    
    def getComputerName(self):
        complete = False
        index = self.numPlayers
        while not complete:
            name = self.computerNames[index]
            complete = True
            for player in self.playerStaging:
                if player.getName() == name:
                    index += 1
                    if index >= len(self.computerNames):
                        index = 0
                        complete = False
            
        return self.computerNames[index]
    
    def getRandomIdentity(self):
        '''For Getting a Random Player for First Turn.'''
        return random.choice(self.players.keys())
    
    def compileMainMenuElements(self):
        def getBlankSpace(word, total):
            return " "*(total-len(word))
        
        def getPlayerBox(playerNum, rowNum):
            if rowNum == 1:
                name = self.playerStaging[playerNum-1].getName()
                return '{}{}'.format(name, getBlankSpace(name, 29))
            elif rowNum == 2:
                points = self.playerStaging[playerNum-1].getPoints()
                return 'Points: {}{}'.format(points, getBlankSpace(str(points), 21))
                
        self.mainMenuElements= {'play1row1':'No Player                    ','play1row2':'                             ',
                                'play2row1':'No Player                    ',
                                'play2row2':'                             ',
                                'play3row1':'No Player                    ','play3row2':'                             ',
                                'play4row1':'No Player                    ',
                                'play4row2':'                             ', 
                                'play1box':'\033[90m','play2box':'\033[90m','play3box':'\033[90m','play4box':'\033[90m',
                                'beginBox':'\033[90m','addBox':'\033[97m','removeBox':'\033[90m'
                                }
        playerBoxKey = 'play{}box'
        playerRowKey = 'play{}row{}'
        i = 1
        for j in self.playerStaging:
            j
            colorCode = ['\033[91m','\033[94m','\033[92m','\033[93m']
            key = playerBoxKey.format(i)
            self.mainMenuElements[key] = colorCode[i-1]
            self.mainMenuElements[playerRowKey.format(i,1)] = getPlayerBox(i, 1)
            self.mainMenuElements[playerRowKey.format(i,2)] = getPlayerBox(i, 2)
            i+=1
        if self.canBegin():
            self.mainMenuElements['beginBox'] = '\033[95m'
        if not self.canAddPlayer():
            self.mainMenuElements['addBox'] = '\033[90m'
        if self.canRemovePlayer():
            self.mainMenuElements['removeBox'] = '\033[97m'
            
    def changeComputerSpeed(self):
        if self.computerSpeed == 'slow':
            self.computerSpeed = 'normal'
        elif self.computerSpeed == 'normal':
            self.computerSpeed = 'fast'
        elif self.computerSpeed == 'fast':
            self.computerSpeed = 'slow'
    
    def getMainMenuElements(self):
        return self.mainMenuElements

class Deck():
    ''''shuffle' (bool) : shuffle deck.'''

    colors =     ('red','yellow','green','blue')
    values =     ('0','1','2','3','4','5','6','7','8','9','X','R','+2')
    
    def __init__(self, populate):
        '''Initializes proper deck of 108 Uno Cards.'''
        self.deck = []
        if populate:
            self.populate(True)
            
    def __getitem__(self, index):
        return self.deck[index]
            
    def populate(self, shuffle=True):
        for color in self.colors:
            for value in self.values:
                self.deck.append(Card(color, value))
                if value != '0':
                    self.deck.append(Card(color, value))
        for i in range(4):
            i #unused
            self.deck.append(Card('wild', '+4'))
            self.deck.append(Card('wild', 'W'))
        if shuffle:
            self.shuffle()

    def __iter__(self):
        return iter(self.deck)

    def __len__(self):
        return len(self.deck)

    def draw(self):
        return self.deck.pop()
    
    def place(self, card):
        return self.deck.append(card)
    
    def insert(self, card):
        self.deck.insert(0, card)

    def shuffle(self):
        random.shuffle(self.deck)

class ComputerPlayer(Player):
    
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Computer'
        self.begun = False
        self.colorsInHand = {'red':0, 'blue':0, 'green':0, 'yellow':0, 'wild':0}
        self.colorsOutHand = {}
        self.currentColor = ""
        
    def addCard(self, card):
        Player.addCard(self, card)
        color = card.getColor()
        self.colorsInHand[color] += 1
        
    def indexCard(self, cardColor, cardValue):
        for card in self.hand:
            if card.getValue() == cardValue:
                if cardValue in ('+4', 'W'):
                    return self.hand.indexCard(card)
                else:
                    if card.getColor() == cardColor:
                        return self.hand.indexCard(card)
        raise ValueError("Card Cannot Be Found")
        
    def think(self, match):
        card = None
        self.currentColor = match.currentColor
        currentValue = match.currentValue
        zeroChangeRule = match.zeroChange
        twoPlayers = False
        previousTurnID = match.getNextTurn(True)
        nextTurnID = match.getNextTurn(False)
        previousPlayer = match.getPlayer(previousTurnID)
        #nextPlayer = match.getPlayer(nextTurnID)
        if previousTurnID == nextTurnID:
            twoPlayers = True
            if self.canSkip == False and self.canReverse == True:
                self.canSkip = True
            self.canReverse = False
        
        self.getLegalCards(self.currentColor, currentValue, zeroChangeRule)

        ### DRAW CASE ###
        
        if len(self.legalCards) == 0 and len(self.wildCards) == 0:
            return "d"
        
        else:
            
            ### NO LEGAL CARD, USE WILD CARD ###
            
            if len(self.legalCards) == 0:
                
                if zeroChangeRule and self.canZeroChange:
                    bestZeroColor = self.getBestColor(self.zeroCards)
                    card = self.getCardByColor(self.zeroCards, bestZeroColor)
                    
                else:
                    
                    if self.canDrawFour:
                        card = self.getCardByValue(self.wildCards, "+4")
                        print(card)
                        
                    else:
                        card = random.choice(self.wildCards)
                
            else:
                
                ### HAS LEGAL CARD ###
                
                if twoPlayers and self.canSkip: #Always play a skip card in a two player game
                    #print("Shed Skip Strategy")
                    card = self.getCardByValue(self.legalCards,"R", "X")
                    
                if self.canReverse and previousPlayer.didDraw():
                    #print("Reverse Strategy")
                    reverseCards = self.getAllCardsByValue(self.legalCards, "R")
                    for reverseCard in reverseCards:
                        if reverseCard.getColor() == self.currentColor:
                            card = reverseCard
                    
                if self.canValueChange:
                    # Computer Can Value Change, However, Should it?
                    # Computer Checks to See if Value Change Color is Better Than Current
                    currentColorNum = self.colorsInHand[self.currentColor]
                    bestValueChangeColor = self.getBestColor(self.valueChangeCards)
                    if self.colorsInHand[bestValueChangeColor] > currentColorNum or len(self.valueChangeCards) == len(self.legalCards):
                        card = self.getCardByColor(self.valueChangeCards, bestValueChangeColor)
                    
                    
                if card == None:
                    #print("Random Strategy")
                    card = random.choice(list(set(self.legalCards) - set(self.valueChangeCards)))
            
        color = card.getColor()
        self.colorsInHand[color] -= 1
        return str(self.indexCard(card.getColor(), card.getValue()))
    
    def getWildColor(self):
        maxKey = max(self.colorsInHand, key=self.colorsInHand.get)
        if maxKey == 'wild':
            return random.choice(('r','g','b','y'))
        else:
            return maxKey
        
    def getCardByValue(self, cardList, *values):
        for card in cardList:
            if card.getValue() in values:
                return card
            
    def getAllCardsByValue(self, cardList, *values):
        cards = []
        for card in cardList:
            if card.getValue() in values:
                cards.append(card)
        return cards
    
    def getCardByColor(self, cardList, *colors):
        for card in cardList:
            if card.getColor() in colors:
                return card
    
    def getBestColor(self, cardList):
        bestColor = None
        bestColorNum = 0
        for card in cardList:
            color = card.getColor()
            if self.colorsInHand[color] > bestColorNum:
                bestColor = color
                bestColorNum = self.colorsInHand[color]
        return bestColor

class Card():
    '''
    'suit' (string) : Card's Color (rgby)
    'rank' (string) : Card's Value (0-9, R, X, W, +2, +4)
    '''

    colors = {
        'red'       :   '\033[91m',
        'green'     :   '\033[92m',
        'yellow'    :   '\033[93m',
        'blue'      :   '\033[94m',
        'purple'    :   '\033[95m',
        'cyan'      :   '\033[96m',
        'white'     :   '\033[97m',
        'wild'      :   '',
        'dwild'     :   '',
        'dred'       :   '\033[31m',
        'dgreen'     :   '\033[32m',
        'dyellow'    :   '\033[33m',
        'dblue'      :   '\033[34m',
        'dpurple'    :   '\033[35m',
        'dcyan'      :   '\033[36m',
        'dwhite'     :   '\033[37m',
    }
    
    idMap = {
        'red':'R','blue':'B','green':'G','yellow':'Y','wild':'W',
        '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9',
        '+2':'+','R':'R','W':'W','+4':'$','X':'X'
    }

    bigNums = {
        "0" : [" .d888b. ","d88P Y88b","888   888","888   888","888   888","888   888","d88P Y88b"," \"Y888P\" "],
        "1" : ["  d888   "," d8888   ","   888   ","   888   ","   888   ","   888   ","   888   "," 8888888 "],
        "2" : [".d8888b. ","d88P  Y88","d8    888","    .d88P",".od888P\" ","d88P\"    ","888\"     ","888888888"],
        "3" : [" .d8888b.","d88P  Y88","     .d88","   8888\" ","     \"Y8b","888    88","Y88b  d88"," \"Y8888P\""],
        "4" : ["    d88b ","   d8P88 ","  d8  88 "," d8   88 ","d8    88 ","888888888","      88 ","      88 "],
        "5" : ["888888888","888      ","888      ","8888888b ","   \"Y88b ","      888","Y88b d88P","\"Y8888P\" "],
        "6" : [" .d888b. ","d88P Y88b","888      ","888d888b ","888P \"Y8b","888   888","Y88b d88b"," \"Y888P\" "],
        "7" : ["888888888","      d8P","     d8P ","    d8P  "," 8888888 ","  d8P    "," d8P     ","d8P      "],
        "8" : [" .d888b. ","d8P   Y8b","Y8b.  d8P"," \"Y8888\" "," .dP\"Yb. ","888   888","Y88b d88P"," \"Y888P\" "],
        "9" : [" .d888b. ","d8P   Y8b","88     88","Y8b.  d88"," \"Y88P888","      888","Y88b d88P"," \"Y888P\" "],
        "X" : ["Y8b   d8P"," Y8b d8P ","  Y8o8P  ","   Y8P   ","   d8b   ","  d888b  "," d8P Y8b ","d8P   Y8b"],
        "W" : ["88     88","88     88","88  o  88","88 d8b 88","88d888b88","88P   Y88","8P     Y8","P       Y"],
        "+2" : ["  db     ","  88     ","C8888D   ","  88 8888","  VP    8","     8888","     8   ","     8888"],
        "+4" : ["  db     ","  88     ","C8888D   ","  88   d ","  VP  d8 ","     d 8 ","    d8888","       8 "],
        "R9" : ["    d88P ","   d88P  ","  d88P   "," d88P    "," Y88b    ","  Y88b   ","   Y88b  ","    Y88b "],
        "R8" : ["   d88P  ","  d88P   "," d88P    ","d88P     ","Y88b     "," Y88b    ","  Y88b   ","   Y88b  "],
        "R7" : ["  d88P  Y"," d88P    ","d88P     ","88P      ","88b      ","Y88b     "," Y88b    ","  Y88b  d"],
        "R6" : [" d88P  Y8","d88P    Y","88P      ","8P       ","8b       ","88b      ","Y88b    d"," Y88b  d8"],
        "R5" : ["d88P  Y88","88P    Y8","8P      Y","P        ","b        ","8b      d","88b    d8","Y88b  d88"],
        "R4" : ["88P  Y88b","8P    Y88","P      Y8","        Y","        d","b      d8","8b    d88","88b  d88P"],
        "R3" : ["8P  Y88b ","P    Y88b","      Y88","       Y8","       d8","      d88","b    d88P","8b  d88P "],
        "R2" : ["P  Y88b  ","    Y88b ","     Y88b","      Y88","      d88","     d88P","    d88P ","b  d88P  "],
        "R1" : ["  Y88b   ","   Y88b  ","    Y88b ","     Y88b","     d88P","    d88P ","   d88P  ","  d88P   "],
        "R0" : [" Y88b    ","  Y88b   ","   Y88b  ","    Y88b ","    d88P ","   d88P  ","  d88P   "," d88P    "],
    }
        

    def __init__(self, color, value):
        '''Initializes Uno Card w/ Color and Value.'''
        self.wild = False       #Is wild card?
        self.zero = False
        self.cardID = '{}{}'.format(self.idMap[color],self.idMap[value])
        self.setColor(color)
        self.setValue(value)
        self.setPoints(value)


    #############################################

    ### -\/-  Retrieve Card Information  -\/- ### 
    
    def __repr__(self):
        return "{},{}".format(self.color, self.value)

    def getBigNum(self, reverse, reverseSeed=0):
        '''Returns list of strings to draw card's value on the pile.'''
        bigNums = []
        colorCode = self.colorCode
        colorCodeDark = self.colorCodeDark
        value = self.value
        if value == 'R':
            if not reverse:
                value += str(reverseSeed)
            else:
                value += str(9-reverseSeed)
        for mid in self.bigNums[value]:
            bigNums += ['{}| |{}'.format(colorCode,colorCodeDark)+mid+'{}| |\033[0m\t'.format(colorCode)]
            
        return bigNums

    def getColor(self):
        '''Returns card's color.'''
        return self.color
    
    def getColorCode(self):
        '''Returns card's color code.'''
        return self.colorCode

    def getValue(self):
        '''Returns card's value.'''
        return self.value
    
    def getPoints(self):
        '''Returns card's point value.'''
        return self.points
    
    def getRow(self,rowNum,hide=False):
        value = self.value
        displaySpace = self.displaySpace
        if hide:
            colorCode = '\033[97m'
            value = '?'
            displaySpace = ' '
        else:
            colorCode = self.colorCode
            if self.isWild():
                if rowNum == 0:  
                    colorCode = '\033[91m'
                elif rowNum == 1:
                    colorCode = '\033[93m'
                elif rowNum == 2:
                    colorCode = '\033[92m'
                elif rowNum == 3:
                    colorCode = '\033[94m'
        
        if rowNum == 0:
            return      '{}\u2666--\u2666\033[0m'.format(colorCode)
        elif rowNum == 1:
            return      '{}|{}{}|\033[0m'.format(colorCode, displaySpace, value)
        elif rowNum == 2:
            if hide:
                return   '{}|? |\033[0m'.format(colorCode)
            else:
                return   '{}|  |\033[0m'.format(colorCode)
        elif rowNum == 3:
            return      '{}\u2666--\u2666\033[0m'.format(colorCode)

    #############################################

    ### -\/-  Set Card Information  -\/- ### 
    
    def setColor(self, color):
        '''Sets Card's color and escape code.'''
        if color == 'blue':
            self.color = 'blue'
            self.colorCode = self.colors['blue']
            self.colorCodeDark = self.colors['dblue']
        elif color == 'red':
            self.color = 'red'
            self.colorCode = self.colors['red']
            self.colorCodeDark = self.colors['dred']
        elif color == 'yellow':
            self.color = 'yellow'
            self.colorCode = self.colors['yellow']
            self.colorCodeDark = self.colors['dyellow']
        elif color == 'green':
            self.color = 'green'
            self.colorCode = self.colors['green']
            self.colorCodeDark = self.colors['dgreen']
        elif color == 'wild':         #No color modification
            self.wild = True
            self.color = 'wild'
            self.colorCodeDark = self.colors['dwild']
            self.colorCode = self.colors['wild']

    def setValue(self, value):
        if value in ('0','1','2','3','4','5','6','7','8','9','X','R','+2','+4','W'):
            self.value = value
            self.displaySpace = ' '
            if len(value) == 2:
                self.displaySpace = ''
            if value == '0':
                self.zero = True
                
    def setPoints(self, value):
        if value in ('0','1','2','3','4','5','6','7','8','9'):
            self.points = int(value)
        elif value in ("W", "+4"):
            self.points = 50
        else:
            self.points = 20


    #############################################

    ### -\/-  Wild Card Methods  -\/- ### 

    def changeColor(self, color):
        '''Changes Card's Color, Intended for Wild Cards.'''
        self.setColor(color)

    def isWild(self):
        '''Returns if card is a wild card.'''
        return self.wild
    
    def isZero(self):
        return self.zero
    
class Match():

    elementsInit = {
        ### Names (final) ###
        'P1Name':'           ', 'P2Name':'           ', 'P3Name':'           ', 'P4Name':'           ',
        ### Card Values ### 
        'P1Cards':'           ', 'P2Cards':'           ', 'P3Cards':'           ', 'P4Cards':'           ',
        ### Turn Colors / Hand###
        'P1Turn':'', 'P2Turn':'', 'P3Turn':'', 'P4Turn':'',
        'HName':'\t\t', 'HVisual':'' ,'Hand':'',
        ### Deck ###
        'DNum':'', 'Deck':['','','','','','','','',''],
        'PostDNum':'',
        ### Pile ###
        'uHeader':'\t\t\t\t', 'uMiddle':'   ', 'uLower':'   ',
        'oHeader':'\t\t\t', 'oMiddle':['\t\t\t','\t\t\t','\t\t\t','\t\t\t','\t\t\t','\t\t\t','\t\t\t','\t\t\t'],
        ### Messages ###
        'Console':'', 'Error':''
        }
    
    speeds = {'slow':2,'normal':1,'fast':0}
        

    def __init__(self, gs):
        ### Decks ###
        self.deck = Deck(True)
        self.pile = Deck(False)
        
        ### Player Information ###
        self.players = gs.players
        self.turnList = []
        self.handTitles =  {'play1':'','play2':'','play3':'','play4':''}
        
        ### Carry Information ###
        self.displayEffects = gs.displayEffects
        self.hideComputerHands = gs.hideComputerHands
        self.zeroChange = gs.zeroChange
        self.computerSpeed = self.speeds[gs.computerSpeed]
        self.simulation = gs.computerSimulation

        ### Data ###
        self.handPosition = 0               # For hand displays
        self.drawAmount = 0                 # Used for force draws
        self.passes = 0                     # Keep track of consecutive passes for emergency color change
        self.passMax = 0                    # Max passes before color change
        self.turn = ''                      # Current turn
        self.event = ''                     # Wild, Reverse, Skip, etc
        self.wildColorChange = ''           # Specifies color to change wild card to
        self.currentColor = ''              # Current color
        self.currentValue = ''              # Current value
        self.winnerID = ''                  # ID of Player who Won
        self.reverse = False                # Is turn order reversed
        self.turnComplete = False           # Is turn complete
        self.matchComplete = False          # Is the Game over?
        self.matchAbort = False             # Did the match conclude without a winner?
        self.forcedWild = False             # Force change wild

        ### Initialize Names / Cards / Deck (Assuming New Game) ###
        self.elements = dict(self.elementsInit)
        
        keyStringName = 'P{}Name'
        keyStringCards = 'P{}Cards'
        
        for i in self.players:
            self.elements[keyStringName.format(i[-1])] = self.players[i].getName()+(' '*(11-len(self.players[i].getName())))
            self.elements[keyStringCards.format(i[-1])] = '  '+(' '*(3-len(str(self.players[i].getCardNum()))))+str(self.players[i].getCardNum())+' Cards'
            
        self.elements['DNum'] = len(self.deck)
        
        if len(str(len(self.deck))) < 2:
            self.elements['PostDNum'] = '\t'
            
        j = 8
        for i in range(int(math.ceil(len(self.deck)/12))):
            self.elements['Deck'][j] = '='
            j -= 1
                    
        for key in GameSettings.playerIdentities:
            try:
                self.buildHandString(key)
                self.turnList += [key]
            except KeyError:
                pass
            
        self.passMax = len(self.turnList)
            
    def clearShell(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def begin(self):
        self.elements['Console'] = 'Beginning Game, Press Enter.'
        print(self.drawScreen())
        self.enterBreak()
        self.eventDealCards()
        self.turn = random.choice(self.turnList)
        self.elements['Console'] = 'First turn will be {}. Press Enter.'.format(self.players[self.turn].getName())
        print(self.drawScreen(True))
        self.enterBreak()
        self.placeCard()
        self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'
        if self.event == 'wild':
            self.eventWildCard()
        elif self.event == 'reverse':
            self.eventReverse()
            
    def end(self, gs):
        if not self.matchAbort:
            points = 0
            self.elements['P{}Turn'.format(self.turn[-1])] = ''
            self.elements['Console'] = '{} Wins! Press Enter to Begin Point Tally'.format(self.players[self.winnerID].getName())
            print(self.drawScreen())
            self.enterBreak()
            
            for identity in self.turnList:
                if identity != self.winnerID:
                    self.turn = identity
                    self.elements['HName'] = self.handTitles[self.turn]
                    self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'
                    while self.players[identity].getCardNum() > 0:
                        card = self.players[identity].removeCard(0)
                        points += card.getPoints()
                        self.elements['Console'] = '{} Won {} Points!'.format(self.players[self.winnerID].getName(),points)
                        
                        keyStringCards = 'P{}Cards'
                        self.elements[keyStringCards.format(identity[-1])] = '  '+(' '*(3-len(str(self.players[identity].getCardNum()))))+str(self.players[identity].getCardNum())+' Cards'
                        self.players[identity].maxScroll = math.ceil((self.players[identity].getCardNum() / 10)-1)
                        if self.handPosition > self.players[identity].maxScroll:
                            self.handPosition -= 1
                        self.buildHandVisual(identity)
                        
                        if self.displayEffects and not self.simulation:
                            print(self.drawScreen())
                            time.sleep(.1)
                    self.elements['P{}Turn'.format(self.turn[-1])] = ''
                        
            self.players[self.winnerID].addPoints(points)
            self.elements['Console'] = '{} Won {} Points! Press Enter'.format(self.players[self.winnerID].getName(),points)
            print(self.drawScreen())
            self.enterBreak()
        
        gs.clearStaging()
        for identity in self.turnList:
            self.players[identity].discardHand()
            gs.addPlayer(self.players[identity])
        return gs
        
    def adjustCardAmount(self, playerID):
        keyStringCards = 'P{}Cards'
        self.elements[keyStringCards.format(playerID[-1])] = '  '+(' '*(3-len(str(self.players[playerID].getCardNum()))))+str(self.players[playerID].getCardNum())+' Cards'
        self.players[playerID].maxScroll = math.ceil((self.players[playerID].getCardNum() / 10)-1)
        if self.handPosition > self.players[playerID].maxScroll:
            self.handPosition -= 1
        self.buildHandVisual(playerID)

    def buildHandString(self, playerID):
        playerName = self.players[playerID].getName()
        if len(playerName) < 9:
            self.handTitles[playerID] = "{}'s Hand\t".format(self.players[playerID].getName())
        else:
            self.handTitles[playerID] = "{}'s Hand".format(self.players[playerID].getName())

    def buildHandVisual(self, playerID):
        string = '['
        for i in range(self.players[playerID].maxScroll+1):
            if i == self.handPosition:
                string += '|'
            else:
                string += '-'
        string += ']'
        self.elements['HVisual'] = string

    def checkInput(self, playerInput):
        if playerInput == '':
            return {'valid':False,'entry':playerInput}
        if playerInput.isnumeric():
            if int(playerInput)+(10*self.handPosition) < self.players[self.turn].getCardNum():
                return {'valid':True,'entry':str(int(playerInput)+(10*self.handPosition)),'type':'card'}
            else:
                self.elements['Error'] = '{} is not a card.'.format(playerInput)
                return {'valid':False,'entry':playerInput}
        else:
            playerInput = playerInput.lower()[0]
            if playerInput in ['<','>','u','d','p','q','s']:
                return {'valid':True,'entry':playerInput}
            else:
                self.elements['Error'] = '{} is not a valid selection.'.format(playerInput)
                return {'valid':False,'entry':playerInput}

    def checkColorInput(self, playerInput):
        if playerInput == '':
            return {'valid':False,'entry':playerInput}
        playerInput = str(playerInput).lower()[0]
        if playerInput[0] == 'b':
            return {'valid':True,'entry':'blue'}
        elif playerInput[0] == 'r':
            return {'valid':True,'entry':'red'}
        elif playerInput[0] == 'g':
            return {'valid':True,'entry':'green'}
        elif playerInput[0] == 'y':
            return {'valid':True,'entry':'yellow'}
        return {'valid':False,'entry':playerInput}

    def eventDealCards(self):
        if self.displayEffects and not self.simulation:
            self.elements['Console'] = 'Dealing Cards...'
        for i in ('play1','play2','play3','play4'):
            if i in self.players:
                for j in range(7):
                    j #unused
                    self.dealCard(i)
                    if self.displayEffects and not self.simulation:
                        print(self.drawScreen(True))
                        time.sleep(.1)

    def eventReverse(self):
        if self.displayEffects and not self.simulation:
            hide = False
            if self.players[self.turn].getType() == "Computer":
                hide = self.hideComputerHands
            self.elements['Console'] = "Reverse Card Played! Reversing Turn Order.".format(self.players[self.turn].getName())
            print(self.drawScreen(hide))
            time.sleep(1)
            for i in range(10):
                cardBigNums = self.pile[0].getBigNum(self.reverse,i)
                self.elements['oMiddle'] = cardBigNums
                print(self.drawScreen(hide))
                if self.displayEffects and not self.simulation:
                    time.sleep(.1)
        cardBigNums = self.pile[0].getBigNum(self.reverse,9)
        self.elements['oMiddle'] = cardBigNums
        self.reverse = not self.reverse
        self.event = ''
            
    def eventSkip(self):
        if self.displayEffects and not self.simulation:
            hide = False
            if self.players[self.turn].getType() == "Computer":
                hide = self.hideComputerHands
            self.elements['Console'] = "Skip Card Placed! Skipping {}'s Turn.".format(self.players[self.turn].getName())
            print(self.drawScreen(hide))
            time.sleep(1)
            for i in range(2):
                i #unused
                self.elements['P{}Turn'.format(self.turn[-1])] = '\033[91m'
                print(self.drawScreen(hide))
                time.sleep(.3)
                self.elements['P{}Turn'.format(self.turn[-1])] = ''
                print(self.drawScreen(hide))
                time.sleep(.3)
        self.turnComplete = True
        self.event = ''

    def eventWildCard(self):
        hide = False
        if not self.forcedWild:
            if self.players[self.turn].getType() == 'Human':
                self.elements['Console'] = 'Wild Card! Specifiy a Color: (B)lue, (R)ed, (G)reen, (Y)ellow'
                self.elements['Error'] = 'Specifiy A Color'
                print(self.drawScreen())
                playerInput = str(input("Color Change: "))
                checked = self.checkColorInput(playerInput)
                while not checked['valid']:
                    if checked['entry'] == '<':
                        self.handPosition -= 1
                        if self.handPosition == -1:
                            self.handPosition = self.players[self.turn].maxScroll
                        self.buildHandVisual(self.turn)
                    elif checked['entry'] == '>':
                        self.handPosition += 1
                        if self.handPosition > self.players[self.turn].maxScroll:
                            self.handPosition = 0
                        self.buildHandVisual(self.turn)
                    print(self.drawScreen())
                    playerInput = str(input("Color Change: "))
                    checked = self.checkColorInput(playerInput)
            else:
                hide = self.hideComputerHands
                checked = self.checkColorInput(self.players[self.turn].getWildColor())
            self.wildColorChange = checked['entry']
        else:
            self.wildColorChange = self.checkColorInput(random.choice(('r','b','g','y')))['entry']
            self.forcedWild = False
        self.currentColor = self.wildColorChange
        self.elements['Error'] = ""
        if self.displayEffects and not self.simulation:
            self.elements['Console'] = 'Wild Card! Changing Color.'
            seed = 1
            for i in range(10):
                i #unused
                if seed > 4:
                    seed = 1
                print(self.drawScreen(hide,wildSeed=seed))
                time.sleep(.1)
                seed += 1
        self.pile[0].changeColor(self.wildColorChange)
        self.wildColorChange = ''
        cardBigNums = self.pile[0].getBigNum(self.reverse)
        self.elements['oHeader'] = '{}\u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t'.format(self.pile[0].getColorCode())
        self.elements['oMiddle'] = cardBigNums
        self.event = ''
        
    def eventDraw(self):
        self.players[self.turn].addForceDraw(self.drawAmount)
        self.drawAmount = 0
        self.event = ''

    def dealCard(self, playerID):
        
        card = self.deck.draw()
        self.players[playerID].addCard(card)
        
        ### Adjust Hand Visual ###
        self.players[playerID].maxScroll = math.ceil((self.players[playerID].getCardNum() / 10)-1)
        self.handPosition = self.players[playerID].maxScroll
        self.buildHandVisual(playerID)
        
        ### Adjust Player Tile ###
        keyStringCards = 'P{}Cards'
        self.elements[keyStringCards.format(playerID[-1])] = '  '+(' '*(3-len(str(self.players[playerID].getCardNum()))))+str(self.players[playerID].getCardNum())+' Cards'
        
        ### Adjust Deck ###
        self.elements['DNum'] = len(self.deck)
        if len(str(len(self.deck))) < 2:
            self.elements['PostDNum'] = '\t'
        j = 8
        self.elements['Deck'] = [' ',' ',' ',' ',' ',' ',' ',' ', ' ']
        for i in range(math.ceil(len(self.deck)/12)):
            i #unused
            self.elements['Deck'][j] = '='
            j -= 1

    def placeCard(self, card=None):
        if card == None:
            ### Used At Beginning For First Card ###
            card = self.deck.draw()
            self.elements['DNum'] = len(self.deck)
            
        cardColor = card.getColorCode()
        cardBigNums = card.getBigNum(self.reverse)
        
        self.currentColor = card.getColor()
        self.currentValue = card.getValue()
        
        self.pile.insert(card)
        self.elements['oHeader'] = '{}\u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t'.format(cardColor)
        self.elements['oMiddle'] = cardBigNums
        
        if len(self.pile) > 1:
            previousCard = self.pile[1]
            previousCardColor = previousCard.getColorCode()
            self.elements['uHeader'] = '{}      \u2666\u2666\u2666=========\u2666\u2666\u2666\033[0m\t\t'.format(previousCardColor)
            self.elements['uMiddle'] = '{}| |\033[0m'.format(previousCardColor)
            self.elements['uLower'] = '{}\u2666\u2666\u2666\033[0m'.format(previousCardColor)
            
        if self.currentColor == 'wild':
            self.event = 'wild'
        
        if self.currentValue == 'X':
            self.event = 'skip'
        elif self.currentValue == 'R':
            if len(self.players) > 2:
                self.event = 'reverse'
            else:
                self.event = 'skip'
        elif self.currentValue == '+4':
                self.drawAmount = 4
        elif self.currentValue == '+2':
                self.drawAmount = 2
        self.passes = 0
                
    def extractCard(self, playerID, index):
        card = self.players[playerID].removeCard(index)
        if self.players[playerID].getCardNum() == 0:
            self.matchComplete = True
            self.winnerID = self.turn
        self.adjustCardAmount(playerID)
        return card
    
    def enterBreak(self):
        if not self.simulation:
            str(input())
        return
            
    def nextTurn(self):
        self.turnComplete = False
        self.handPosition = 0
        turnType = self.players[self.turn].getType()
        self.players[self.turn].beginTurn()
        ### Prepare Hand Visuals ###
        
        self.elements['HName'] = self.handTitles[self.turn]
        self.buildHandVisual(self.turn)
        
        if self.event == 'skip':
            self.eventSkip()
        elif self.drawAmount > 0:
            self.eventDraw()
        
        while not self.turnComplete:
            if turnType == 'Human':
                self.players[self.turn].getLegalCards(self.currentColor, self.currentValue, self.zeroChange)
                if len(self.deck) > 0:
                    self.elements['Console'] = 'Select a card, (D)raw, or (P)ause.'
                else:
                    self.players[self.turn].removeForceDraw()
                    self.elements['Console'] = 'Select a card, (D)raw, (P)ause, or Pas(s).'
                if self.players[self.turn].getForceDraws() > 0:
                    self.elements['Error'] = 'Draw Card Played! Draw {} cards.'.format(self.players[self.turn].getForceDraws())
                print(self.drawScreen())
                playerInput = str(input("\033[97mSelection: \033[92m"))
                checked = self.checkInput(playerInput)
                while not checked['valid']:
                    print(self.drawScreen())
                    playerInput = str(input("\033[97mSelection: \033[92m"))
                    checked = self.checkInput(playerInput)
    
                playerInput = checked['entry']
                
                if playerInput == '<':
                    self.handPosition -= 1
                    if self.handPosition == -1:
                        self.handPosition = self.players[self.turn].maxScroll
                    self.buildHandVisual(self.turn)
                elif playerInput == '>':
                    self.handPosition += 1
                    if self.handPosition > self.players[self.turn].maxScroll:
                        self.handPosition = 0
                    self.buildHandVisual(self.turn)
                elif playerInput == 'd':
                    if len(self.deck) > 0:
                        self.elements['Error'] = ''
                        self.dealCard(self.turn)
                    else:
                        self.elements['Error'] = "Cannot Draw. Deck is Empty"
                elif playerInput == 'p':
                    pauseOutput = self.pauseScreen()
                    if pauseOutput == 'quit':
                        self.matchComplete = True
                        self.turnComplete = True
                        self.winnerID = 'play1'
                        self.matchAbort = True
                elif playerInput == 's':
                    if len(self.deck) > 0:
                        self.elements['Error'] = "Cannot pass until Deck is empty."
                    elif len(self.players[self.turn].getAllValidCards()) > 0:
                        self.elements['Error'] = "Cannot pass while having playable cards."
                    else:
                        self.turnComplete = True
                        self.passes += 1
                        if self.passes == self.passMax:
                            self.forcedWild = True
                            self.event = 'wild'
                            self.passes = 0
                elif playerInput.isnumeric():
                    if self.players[self.turn].getForceDraws() == 0:
                        cardCheck = self.players[self.turn].checkCard(playerInput)
                        if cardCheck in self.players[self.turn].getAllValidCards():
                            card = self.extractCard(self.turn, playerInput)
                            self.placeCard(card)
                            self.elements['Error'] = ""
                            self.turnComplete = True
                        else:
                            self.elements['Error'] = "Card Doesn't Match The Color {} or Value {}!".format(self.currentColor, self.currentValue)
                    else:
                        pass
                    
            elif turnType == 'Computer':
                self.elements['Console'] = '{}\'s Turn'.format(self.players[self.turn].getName())
                print(self.drawScreen(self.hideComputerHands))
                if not self.simulation:
                    time.sleep(self.computerSpeed)
                #str(input())
                while (True):
                    if self.displayEffects and not self.simulation:
                        time.sleep(.2)
                    if self.players[self.turn].getForceDraws() > 0 and len(self.deck) > 0:
                        cardIndex = 'd'
                    else:
                        cardIndex = self.players[self.turn].think(self)
                    if cardIndex.isnumeric():
                        card = self.extractCard(self.turn, int(cardIndex))
                        if card.getColor() != self.currentColor:
                            self.resetDrawBool()
                        self.placeCard(card)
                        self.turnComplete = True
                        break
                    else:
                        if cardIndex == 'd':
                            if len(self.deck) > 0:
                                self.dealCard(self.turn)
                                print(self.drawScreen(self.hideComputerHands))
                            else:
                                self.turnComplete = True
                                self.players[self.turn].removeForceDraw()
                                self.passes += 1
                                if self.passes == self.passMax:
                                    self.forcedWild = True
                                    self.event = 'wild'
                                    self.passes = 0
                                break
                
            ### DECODE INPUT ###
                
        if self.event == 'reverse':
            self.eventReverse()
        elif self.event == 'wild':
            self.eventWildCard()
            
        # Clear Current Turn
        self.elements['P{}Turn'.format(self.turn[-1])] = ''
        # Prepare Next Turn
        self.turn = self.getNextTurn()
        self.elements['P{}Turn'.format(self.turn[-1])] = '\033[93m'

    def drawScreen(self, hide=False, wildSeed=0):
        if self.simulation:
            return ''
        colorCombos = {
            1 : ['\033[91m','\033[93m','\033[92m','\033[94m'],
            2 : ['\033[94m','\033[91m','\033[93m','\033[92m'],
            3 : ['\033[92m','\033[94m','\033[91m','\033[93m'],
            4 : ['\033[93m','\033[92m','\033[94m','\033[91m'] }
        currentTurn = self.turn
        if currentTurn == '':
            currentTurn = self.turnList[-1]
            hide = True
        if wildSeed != 0:
            colorMod = colorCombos[wildSeed]
        else:
            colorMod = ['','','','']

        self.clearShell()
        screenout = ''
        screenout += '\t\t\033[94m      || ||\033[92m ||\ ||  \033[91m// \\\\\n\033[0m'
        screenout += '\t\t\033[94m      || ||\033[92m ||\\\|| \033[91m((   ))\n\033[0m'
        screenout += '\t\t\033[94m      \\\ //\033[92m || \|| \033[91m \\\ //\n\033[0m'
        screenout += '\033[97m===============================================================\n'
        screenout += '\033[93m{}\033[0m\n'.format(self.elements['Console'])
        screenout += '\033[97m===============================================================\n'
        screenout += '\t\t\t\t\t\t'     +        ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P1Turn'])
        screenout += '\033[97mDeck:\t\t'        +       '{}'.format(self.elements['uHeader'])       +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P1Turn'],self.elements['P1Name'])
        screenout += '\033[97m{} Cards'.format(self.elements['DNum'])       +       '{}'.format(self.elements['PostDNum'])+'\t'     +       '{}'.format(self.elements['uHeader'])       +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P1Turn'],self.elements['P1Cards'])
        screenout += '\t\t      '       +      '{}'.format(self.elements['uMiddle'])        +       '\033[97m{}{}'.format(colorMod[0],self.elements['oHeader'])     +      ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P1Turn'])
        screenout += '\033[97m  _+_ \t\t      '     +       '{}'.format(self.elements['uMiddle'])                                                                                                   +       '\033[97m{}{}'.format(colorMod[1],self.elements['oHeader'])         +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P2Turn'])                                                                                  
        screenout += '\033[97m | '      +       '\033[92m{}\033[0m'.format(self.elements['Deck'][0])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[2],self.elements['oMiddle'][0])      +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P2Turn'],self.elements['P2Name'])
        screenout += '\033[97m | '      +       '\033[92m{}\033[0m'.format(self.elements['Deck'][1])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[3],self.elements['oMiddle'][1])      +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P2Turn'],self.elements['P2Cards'])
        screenout += '\033[97m | '      +       '\033[92m{}\033[0m'.format(self.elements['Deck'][2])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[0],self.elements['oMiddle'][2])      +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P2Turn'])
        screenout += '\033[97m | '      +       '\033[93m{}\033[0m'.format(self.elements['Deck'][3])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[1],self.elements['oMiddle'][3])      +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P3Turn'])
        screenout += '\033[97m | '      +       '\033[93m{}\033[0m'.format(self.elements['Deck'][4])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[2],self.elements['oMiddle'][4])      +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P3Turn'],self.elements['P3Name'])
        screenout += '\033[97m | '      +       '\033[93m{}\033[0m'.format(self.elements['Deck'][5])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uMiddle'])       +       '\033[97m{}{}'.format(colorMod[3],self.elements['oMiddle'][5])      +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P3Turn'],self.elements['P3Cards'])
        screenout += '\033[97m | '      +       '\033[91m{}\033[0m'.format(self.elements['Deck'][6])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uLower'])        +       '\033[97m{}{}'.format(colorMod[0],self.elements['oMiddle'][6])      +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P3Turn'])
        screenout += '\033[97m | '      +       '\033[91m{}\033[0m'.format(self.elements['Deck'][7])        +       '\033[97m |\t\t      '      +       '{}'.format(self.elements['uLower'])        +       '\033[97m{}{}'.format(colorMod[1],self.elements['oMiddle'][7])      +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P4Turn'])
        screenout += '\033[97m |_'      +     '\033[91m{}\033[0m'.format(self.elements['Deck'][8])          +        '\033[97m_|\t\t         '                                                      +      '\033[97m{}{}'.format(colorMod[2],self.elements['oHeader'])          +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P4Turn'],self.elements['P4Name'])
        screenout += '\033[97m\t\t         '    +                                                                                                                                                                   '\033[97m{}{}'.format(colorMod[3],self.elements['oHeader'])         +       ' \033[97m{}|{}|\033[0m\n'.format(self.elements['P4Turn'],self.elements['P4Cards'])
        screenout += '\t\t\t\t\t\t'     +       ' \033[97m{}\u2666-----------\u2666\033[0m\n'.format(self.elements['P4Turn'])
        screenout += "\033[97m{}".format(self.elements['HName'])        +       "\t\t\t\t {}\n".format(self.elements['HVisual'])
        screenout += '\033[97m===============================================================\n'
        screenout += self.players[currentTurn].getHand(self.handPosition,hide)
        screenout += '\033[91m{}\033[0m'.format(self.elements['Error'])
        return screenout
    
    def pauseScreen(self):
        while True:
            self.clearShell()
            print('\n\t\t\tPause')
            print('\n\t\t1. Resume')
            print('\t\t2. Quit')
            
            selection = str(input('\nSelection: ')).upper()
            while selection not in ['1', '2']:
                print('\nSelection Invalid')
                selection = str(input('\nSelection: ')).upper()
                
            if selection == '1' or "":
                return ""
                
            elif selection == '2':
                return "quit"
                
    
    def isComplete(self):
        return self.matchComplete
    
    def next(self):
        self.turn = self.getNextTurn()
    
    def getNextTurn(self, forceReverse=False):
        if forceReverse:
            reverse = not self.reverse
        else:
            reverse = self.reverse
        currentIndex = self.turnList.index(self.turn)
        if not reverse:
            if (currentIndex + 1) == len(self.turnList):
                return self.turnList[0]
            else:
                return self.turnList[currentIndex+1]
        else:
            if currentIndex == 0:
                return self.turnList[len(self.turnList) - 1]
            else:
                return self.turnList[currentIndex-1]
            
    def getPlayer(self, playerID):
        return self.players[playerID]
    
    def resetDrawBool(self):
        for identity in self.players:
            self.players[identity].drew = False

def Uno(debugging=False):

    ###MENUS###
    
    def clearShell():
        os.system('cls' if os.name == 'nt' else 'clear')

    def mainMenu():
        sys.stdout.write("\x1b[8;32;63t")
        sys.stdout.flush()
        gs = GameSettings()
        
        while True:
 
            print(drawMainMenu(gs))
            
            selection = str(input('\033[97mSelection: \033[92m'))
            while selection not in ['1', '2', '3', '4', '5']:
                gs.mainMenuError = "Invalid Selection"
                print(drawMainMenu(gs))
                selection = str(input('\033[97mSelection: \033[92m'))
                
            if selection == '1':
                if gs.canBegin():
                    gs.mainMenuError = ""
                    gs.finalizePlayers()
                    gs = playMatch(gs)
                else:
                    gs.mainMenuError = "Two Players Required to Begin"

            elif selection == '2':
                if gs.canAddPlayer():
                    gs.mainMenuError = ""
                    gs = addPlayer(gs)
                else:
                    gs.mainMenuError = "Max Number of Players Reached"
                    
            elif selection == '3':
                if gs.canAddPlayer():
                    gs.mainMenuError = ""
                    gs = addComputer(gs)
                else:
                    gs.mainMenuError = "Max Number of Players Reached"

            elif selection == '4':
                if gs.canRemovePlayer():
                    gs.mainMenuError = ""
                    gs = removePlayer(gs)
                else:
                    gs.mainMenuError = "No Players to Remove"

            elif selection == '5':
                gs.mainMenuError = ""
                gs = settingsMenu(gs)

            else:
                raise BadInputError('Data Provided Has No Function')
            
    def playMatch(gs):
        for i in range(1):
            i
            m = Match(gs)
            m.begin()
            while (not m.isComplete()):
                m.nextTurn()
            gs = m.end(gs)
        return gs
            
    def addPlayer(gs):
        colors = ['\033[91m','\033[94m', '\033[92m', '\033[93m']
        nameOkay = False
        playerNum = gs.getPlayerNum() + 1
        colorIndex = playerNum - 1
        message = "\033[97mPlease Enter Player {}'s Name: {}".format(playerNum, colors[colorIndex])
        
        while not nameOkay:
            print(drawMainMenu(gs))
            name = str(input(message)).title()
            if len(name) > 11:
                gs.mainMenuError = "Name Must Be 11 Characters or Less!"
            elif len(name) == 0:
                gs.mainMenuError = ""
                return gs
            else:
                nameOkay = True
                for player in gs.playerStaging:
                    if player.getName() == name:
                        nameOkay = False
                if nameOkay == False or name in GameSettings.computerNames:
                    gs.mainMenuError = "Name Cannot Match Another Player's Name!"
                        
        p = Player(name)
        gs.addPlayer(p)
        gs.mainMenuError = ""
        
        return gs
    
    def addComputer(gs):
        name = gs.getComputerName()
        c = ComputerPlayer(name)
        gs.addPlayer(c)
        
        return gs
    
    def removePlayer(gs):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=63))
        sys.stdout.flush()
        clearShell()
        
        complete = False
        playerNum = gs.getPlayerNum()
        message = "\033[97mPlease Enter Player Number to Remove: \033[91m".format(playerNum)
        
        while (not complete):
            print(drawMainMenu(gs))
            number = str(input(message)) 
            if len(number) == 0:
                gs.mainMenuError = ""
                return gs
            try:
                number = int(number)
                if 0 < number <= playerNum:
                    complete = True
                else:
                    gs.mainMenuError = "Invalid Player Number!"
            except:
                gs.mainMenuError = "Please Enter the Player Number, not Name!"
        
        gs.mainMenuError = ""
        gs.removePlayer(number)
        return gs
    
    def settingsMenu(gs):
        while True:
            sys.stdout.write("\x1b[8;32;63t")
            sys.stdout.flush()
            clearShell()
            print('\n\t\tSettings')
            print('\n\t1. Draw Effects\t\t\t{}'.format(gs.displayEffects))
            print('\t2. Hide Computer Hands\t\t{}'.format(gs.hideComputerHands))
            print('\t3. Computer Speed\t\t{}'.format(gs.computerSpeed.title()))
            #print('\t4. Zero Card Changes Color\t{}'.format(gs.zeroChange))
            #print('\t5. Run Simulations\t\t{}'.format(gs.computerSimulation))
            print('\n\tA. Exit')
            
            selection = str(input('\nSelection: ')).upper()
            while selection not in ('1', '2', '3', '4', '5', 'A', ''):
                print('\nSelection Invalid')
                selection = str(input('\nSelection: ')).upper()
                
            if selection == '1':
                gs.displayEffects = not gs.displayEffects
                
            elif selection == '2':
                gs.hideComputerHands = not gs.hideComputerHands
                
            elif selection == '3':
                gs.changeComputerSpeed()
                '''
            elif selection == '4':
                gs.zeroChange = not gs.zeroChange
                
            elif selection == '5':
                gs.computerSimulation = not gs.computerSimulation
                '''
            elif selection == 'A' or selection == '' or selection in ('4','5'):
                return gs
    
    def drawMainMenu(gs):
        clearShell()
        gs.compileMainMenuElements()
        menuElements = gs.getMainMenuElements()
        screenout = ''
        screenout += '\t\t\033[94m      || ||\033[92m ||\ ||  \033[91m// \\\\\n\033[0m'
        screenout += '\t\t\033[94m      || ||\033[92m ||\\\|| \033[91m((   ))\n\033[0m'
        screenout += '\t\t\033[94m      \\\ //\033[92m || \|| \033[91m \\\ //\n\033[0m'
        screenout += '\033[97m===============================================================\033[0m\n'
        screenout += "{}1-----------------------------1\033[0m {}2-----------------------------2\033[0m\n".format(menuElements['play1box'],menuElements['play2box'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play1box'],menuElements['play1row1'],menuElements['play2box'],menuElements['play2row1'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play1box'],menuElements['play1row2'],menuElements['play2box'],menuElements['play2row2'])
        screenout += "{}1-----------------------------1\033[0m {}2-----------------------------2\033[0m\n".format(menuElements['play1box'],menuElements['play2box'])
        screenout += "{}3-----------------------------3\033[0m {}4-----------------------------4\033[0m\n".format(menuElements['play3box'],menuElements['play4box'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play3box'],menuElements['play3row1'],menuElements['play4box'],menuElements['play4row1'])
        screenout += "{}|{}|\033[0m {}|{}|\033[0m\n".format(menuElements['play3box'],menuElements['play3row2'],menuElements['play4box'],menuElements['play4row2'])
        screenout += "{}3-----------------------------3\033[0m {}4-----------------------------4\033[0m\n".format(menuElements['play3box'],menuElements['play4box'])
        screenout += "\033[97m===============================================================\033[0m\n"
        screenout += "  {}\u2666---------------------------\u2666\033[0m \u2666===========================\u2666\n".format(menuElements['beginBox'])
        screenout += "  {}|1.       Begin Match       |\033[0m |        High Scores        |\n".format(menuElements['beginBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m \u2666---------------------------\u2666\n".format(menuElements['beginBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}|2.       Add Player        |\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}|3.      Add Computer       |\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['addBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['removeBox'])
        screenout += "  {}|4.      Remove Player      |\033[0m |                           |\n".format(menuElements['removeBox'])
        screenout += "  {}\u2666---------------------------\u2666\033[0m |                           |\n".format(menuElements['removeBox'])
        screenout += "  \033[97m\u2666---------------------------\u2666\033[0m |                           |\n"
        screenout += "  \033[97m|5.        Settings         |\033[0m |                           |\n"
        screenout += "  \033[97m\u2666---------------------------\u2666\033[0m \u2666===========================\u2666\n"
        screenout += "\033[97m===============================================================\033[0m\n"
        screenout += '\033[91m{}\033[0m'.format(gs.mainMenuError)
        return screenout
    
    mainMenu()
            
if __name__ == "__main__":
    Uno()
        
