# PREAMBLE



# My original intention was to create some

# disruptive visual camoflage, inspired by the pattern on

# the bark of plane trees. The result was never quite what I intended

# and several fixes had to be incorperated to aproximate what I wanted.

# The end result is effective though and reminds me of a Jackson Pollock

# or a Monet painting.



# CODE



from Tkinter import *

from math import *

from random import*



# critical parameters, adjust to suit



W = 900     # canvas dimensions

H = 500     

nLow    = 25   # recursive limiter

nLayers = 5    # number of repeated paint overs

nCover  = 0.8  # Adjusts probability of a particular area being painted over per sweep

nMSpan  = 5.0  # Same as above, These two parameters depend upon the number of recursions

nCSpan  = 2.0  # Same for colour range

# scale factor per recursion. i.e. not scale invariant

aScale  = [0.1, .3, .5, 0.5,0.9,0.9,0.1,0.1,0.1,0,0,0,0,0,0,0,0,0,0,0,0]

# colours are scale invariant

aColour = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]



# The two functions AutumnPastels and DrawSplash

# can be modified to suit 

def AutumnPastels(nCR, nCG, nCB):

    # colour scheme

    cR = ColStr(int((ZeroToOne(nCR, 8.0)) * 150) + 80) # red   

    cG = ColStr(int((ZeroToOne(nCG, 8.0)) * 150) + 80) # green 

    cB = ColStr(int((ZeroToOne(nCB, 8.0)) * 25) + 30)  # blue                     

    return '#' + cR + cG + cB                         



def DrawSplash(nX, nY, colour):

    # simulation of paint splatter or leaves

    nX2 = dist(nX, nLow / 2.0)

    nY2 = dist(nY, nLow / 2.0)

    for i in range(8):

        nX1 = dist(nX2, nLow / 3.0)

        nY1 = dist(nY2, nLow / 3.0)

        nL  = dist(nLow / 6.0 + 2, nLow / 3.0)

        canvas.create_oval( nX1, nY1, nX1 + nL, nY1 + nL, fill = colour, width = 0)

    canvas.update()





def ColStr( x):

    if x > 255:

        x = 0

    if x < 0:

        x = 255

    s = "%x" % x # converts x into a hexidecimal string

    if len( s) < 2:

        s = '0' + s

    return s



# This is a clumbsy way of recording continuity across the plane

# A dictionary would be more efficient, but it seems to work O.K.

def Load(aGrid, nX, nY, n):

    # changes value if not set, or else it returns the value

    if aGrid[nX][nY] == -1:

       aGrid[nX][nY] = n

       return n

    return aGrid[nX][nY]





def ZeroToOne(nM, nSpan):

    # maps the Real domain onto [0 , 1]

    return atan(nM * nSpan) / pi + 0.5 

    

def mid(n1, n2):

    return int((n1 + n2) / 2) 





def dist(nP, nScale):

    return nP + (random() - 0.5) * nScale





def FracDown(aGrid, nX1, nY1, nX2, nY2, nTL, nTR, nBL, nBR, nLim, nRecursive, nCR, nCG, nCB):          

    # fractal lanscape grenerator

    dx = nX2 - nX1

    dy = nY2 - nY1

    nS = aScale[nRecursive]

    nT = dist((nTL + nTR) / 2, nS * nHorizFactor)

    nL = dist((nTL + nBL) / 2, nS)

    nR = dist((nTR + nBR) / 2, nS)

    nB = dist((nBL + nBR) / 2, nS * nHorizFactor)

    nM = dist((nTL + nTR + nBL + nBR) / 4, nS * nDiagFactor)

    nSC = aColour[nRecursive]

    nCR = dist(nCR, nSC)

    nCG = dist(nCG, nSC)

    nCB = dist(nCB, nSC)

    nXm = mid(nX1, nX2)

    nYm = mid(nY1, nY2)



    if dx <= nLow and dy <= nLow: 

       if ZeroToOne(nM, nMSpan) > nLim:

           DrawSplash(nXm, nYm, AutumnPastels(nCR, nCG, nCB))

       return

    nTL = Load(aGrid, nX1, nY2, nTL)

    nTR = Load(aGrid, nX2, nY2, nTR)

    nBL = Load(aGrid, nX1, nY1, nBL)

    nBR = Load(aGrid, nX1, nY1, nBR)

    t1  = (aGrid, nX1, nYm, nXm, nY2, nTL, nT,  nL,  nM,  nLim, nRecursive + 1, nCR, nCG, nCB)          

    t2  = (aGrid, nXm, nYm, nX2, nY2, nT,  nTR, nM,  nR,  nLim, nRecursive + 1, nCR, nCG, nCB)          

    t3  = (aGrid, nX1, nY1, nXm, nYm, nL,  nM,  nBL, nB,  nLim, nRecursive + 1, nCR, nCG, nCB)          

    t4  = (aGrid, nXm, nY1, nX2, nYm, nM,  nR,  nB,  nBR, nLim, nRecursive + 1, nCR, nCG, nCB)          

    aT  = [t1,t2,t3,t4]

    shuffle(aT)

    for i in aT:

        apply(FracDown, i)



def Frac(nLim):

    aGrid = []

    for i in range(W):

        aGrid.append([-1] * H)

    FracDown(aGrid, 0, 0, W - 1, H - 1, 0.0, 0.0, 0.0, 0.0,nLim, 1, 0.0, 0.0, 0.0)          



seed()

canvas = Canvas( width = W, height = H)

canvas.pack(side = TOP)

canvas.create_rectangle( 0, 0, W, H, fill = AutumnPastels(-0.8, -0.4, -3.0), width = 0, tag ='o')

nHorizFactor = (W + 0.0) / (H + 0.0)

nDiagFactor  = sqrt(H**2 + W**2) / (H + 0.0) 

for i in range(nLayers):

    Frac(nCover)

print 'done'    
