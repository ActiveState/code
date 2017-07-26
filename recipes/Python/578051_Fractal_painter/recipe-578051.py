# PREAMBLE



# My original intention was to create some

# disruptive visual camoflage, inspired by the pattern on

# the bark of plane trees. The result was never quite what I intended

# and several fixes had to be incorperated to aproximate what I wanted.

# The end result is effective though and reminds me of a Jackson Pollock

# or a Monet painting.

# I think that the program does quite a good job of producing an aesteticalty

# pleasing picture, through a purely mathematical process,

# though some considerable tweeking on the part of the programmer

# was needed to achieve this.

# In this version, I am able to show a wide variety of colour schemes.

# Artists code their colours according to three dimensions, (hue, chorma and saturation)

# This might be a more apropriate approach than (red, green, blue).



# CODE



from Tkinter import *

from math import *

from random import*



# critical parameters, adjust to suit

W = 800        # canvas dimensions

H = 500        # golden ratio  

nLow    = 25   # recursive limiter

nCover  = 0.05  # Adjusts probability of a particular area being painted over per sweep

nMSpan  = 10.0  # Same as above, These two parameters depend upon the number of recursions

nCSpan  = 8.0  # Same for colour range

nSplatterSize = 0.25

# scale factor per recursion. i.e. not scale invariant

aScale  = [0.05, .1, .6, 0.9,0.9,0.3,0.1,0.1,0.1,0,0,0,0,0,0,0,0,0,0,0,0]

# colours 

aColour = [0.5,0.0,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]



# The two functions VibrantHousePaint and DrawDrip

# can be modified to suit 

def VibrantHousePaint(oM, nR):

    # colour scheme

    rg  = oM.rg

    rb  = oM.rb

    gb  = oM.gb

    cR = ColStr(int((ZeroToOne(oM.r + rg - rb - oM.rgb , nCSpan * nR)) * nMaxR) + nMinR) # red   

    cG = ColStr(int((ZeroToOne(oM.g - rg + gb - oM.rgb , nCSpan * nR)) * nMaxG) + nMinG) # green 

    cB = ColStr(int((ZeroToOne(oM.b + gb - rb - oM.rgb , nCSpan * nR)) * nMaxB) + nMinB) # blue              

    return '#' + cR + cG + cB                         



def DrawDrip(nX, nY, oM, nR, bScheme):

    colour = apply(bScheme, (oM, nR))

    nL = (nLow + 0.0) * nR / 3

    nX1 = dist(nX, nL * nSplatterSize)

    nY1 = dist(nY, nL * nSplatterSize)

    nL2 = dist(nL , nL)

    canvas.create_oval( nX1, nY1, nX1 + nL2, nY1 + nL2, fill = colour, width = 0)

    canvas.create_rectangle( nX1, nY1 , nX1 + nL2 / 2.0, nY1 + nL2 / 2.0, fill = colour, width = 0)

    canvas.update()





class splat:

    def __init__(self,z,r,g,b,rg,rb,gb,rgb):

        self.z   = z

        self.r   = r

        self.g   = g

        self.b   = b

        self.rg  = rg

        self.rb  = rb

        self.gb  = gb

        self.rgb = rgb



def ColStr( x):

    if x > 255:

        x = 0

    if x < 0:

        x = 255

    s = "%x" % x # converts x into a hexidecimal string

    if len( s) < 2:

        s = '0' + s

    return s



def Load(aGrid, nX, nY, n):

    # changes value if not set, or else it returns the value

    cKey = str( nX) + '_' + str( nY)

    if aGrid.has_key(cKey):

       return aGrid[cKey]

    aGrid[cKey] = n

    return n





def ZeroToOne(nM, nSpan):

    # maps the Real domain onto [0 , 1]

    return atan(nM * nSpan) / pi + 0.5 

    

def mid(n1, n2):

    return int((n1 + n2) / 2) 



def dist(nP, nScale):

    return nP + (random() - 0.5) * nScale



def odist(A, nS1, nS2):

    z = 0

    r = 0

    g = 0

    b = 0

    h = 0

    v = 0

    rg = 0

    rb = 0

    gb = 0

    rgb = 0

    for i in A:

        z += i.z

        r += i.r

        g += i.g

        b += i.b

        rg += i.rg

        rb += i.rb

        gb += i.gb

        rgb += i.rgb

    l = len(A)

    z = dist(z / l, nS1)

    r = dist(r / l, nS2)

    g = dist(g / l, nS2)

    b = dist(b / l, nS2)

    rg = dist(rg / l, nS2)

    rb = dist(rb / l, nS2)

    gb = dist(gb / l, nS2)

    rgb = dist(rgb / l, nS2)

    return splat(z, r, g, b, rg, rb, gb, rgb)



def FracDown(aGrid, nX1, nY1, nX2, nY2, oTL, oTR, oBL, oBR, nLim, nRecursive, bScheme):          

    # fractal lanscape grenerator

    dx  = nX2 - nX1

    dy  = nY2 - nY1

    nS  = aScale[nRecursive]

    nSC = aColour[nRecursive]

    oT  = odist([oTL, oTR], nS * nHorizFactor, nSC)

    oL  = odist([oTL, oBL], nS, nSC)

    oR  = odist([oTR, oBR], nS, nSC)

    oB  = odist([oBL, oBR], nS * nHorizFactor, nSC)

    oM  = odist([oTL, oTR, oBL, oBR], nS * nDiagFactor, nSC)

    nXm = mid(nX1, nX2)

    nYm = mid(nY1, nY2)

    oTL = Load(aGrid, nX1, nY2, oTL)

    oTR = Load(aGrid, nX2, nY2, oTR)

    oBL = Load(aGrid, nX1, nY1, oBL)

    oBR = Load(aGrid, nX1, nY1, oBR)



    if dx <= nLow and dy <= nLow: 

       if ZeroToOne(oM.z, nMSpan * sqrt(nRecursive)) > nLim:

           DrawDrip(nXm, nYm, oM, sqrt(nRecursive), bScheme)

       return

    t1  = (aGrid, nX1, nYm, nXm, nY2, oTL, oT,  oL,  oM,  nLim, nRecursive + 1, bScheme)          

    t2  = (aGrid, nXm, nYm, nX2, nY2, oT,  oTR, oM,  oR,  nLim, nRecursive + 1, bScheme)          

    t3  = (aGrid, nX1, nY1, nXm, nYm, oL,  oM,  oBL, oB,  nLim, nRecursive + 1, bScheme)          

    t4  = (aGrid, nXm, nY1, nX2, nYm, oM,  oR,  oB,  oBR, nLim, nRecursive + 1, bScheme)          

    aT  = [t1,t2,t3,t4]

    shuffle(aT)

    for i in aT:

        apply(FracDown, i)





def ColourRange():

    nMin = int(random() * 255)

    nMax = int(random() * 255)

    if nMin > nMax:

       nMin, nMax = nMax, nMin

    return nMin, nMax - nMin



def Frac(nLim, bScheme):

    aGrid = {}

    s1 = splat(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

    s2 = splat(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

    s3 = splat(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

    s4 = splat(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

    FracDown(aGrid, 0, 0, W - 1, H - 1, s1, s2, s3, s4,nLim, 1, bScheme)          



seed()

canvas = Canvas( width = W, height = H)

canvas.pack(side = TOP)

canvas.create_rectangle( 0, 0, W, H, fill = 'gray', width = 0)

nHorizFactor = (W + 0.0) / (H + 0.0)

nDiagFactor  = sqrt(H**2 + W**2) / (H + 0.0) 

nMinR, nMaxR = ColourRange()

nMinG, nMaxG = ColourRange()

nMinB, nMaxB = ColourRange()

Frac(nCover, VibrantHousePaint)

print 'done'    
