# This progam creates a non periodic tiling of the plane using 'Penrose tiles',
# wich were invented by Roger Penrose.
# Each time it runs it will generate a new random pattern.
# There are an infinite number of them.
# Unlike a periodic tesselation the assembly requires forward planning and
# hence the program searches through various combinations of parts, often
# comming to a dead end and having to backtrack.
# The program has three phases, the first generating the initial layout with
# a simple sharks tooth design
# The second fills in the tiles completely
# The third phase reveals an inner fractal pattern by the process of deflation
# then deflating again over and over
# You must close the progam to stop it.
from __future__ import division
from Tkinter import * 
from math import cos, sin, atan2, sqrt, pi
from random import random, shuffle, seed
from numpy import array, dot, transpose
from copy import deepcopy
from sys import getrecursionlimit, setrecursionlimit

nW = 800.0 # change these to make the screen bigger or smaller
nH = 600.0
canvas = Canvas( width = nW, height = nH, bg = 'darkred')
canvas.pack(expand = YES, fill = BOTH)

# setrecursionlimit(10000)
nRecLim = getrecursionlimit()
nScale = 30.0 # sqrt(nW * nH / nRecLim) / nFib #25.0 # change this to make the tile bigger or smaller
nFib   = (1.0 + sqrt(5.0))/2.0 # Fibonacci's golden ratio
nSmall = 5 # the smallest possible gap should be 18`
n36    = 36.0 * pi / 180.0
nSin36 = sin(n36)
nCos36 = cos(n36)
n72    = 72.0 * pi / 180.0
nSin72 = sin(n72)
nCos72 = cos(n72)
nSelfX = nScale * nFib * nSin36
nSelfY = nScale * nFib * nCos36
nW2 = nW / 2
nH2 = nH / 2
nTag = 0
nRatioSmall = nScale * nFib / (nFib + 1)
nRatioBig   = nScale * nFib**2 / (nFib + 1)
lAlternate = False    
def NewTag():
    global nTag
    nTag += 1
    return "TAG%d" %(nTag)

def Scalar(midx, midy, nR, x0, y0):
    midx -= x0
    midy -= y0
    midR = sqrt(midx**2 + midy**2)
    if midR == 0:
        return [x0, y0]
    midx *= nR / midR
    midy *= nR / midR
    midx += x0
    midy += y0
    return [midx,midy]

def MidArc(p1, p2, p0, nR):
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0] 
    y1 = p1[1] 
    x2 = p2[0] 
    y2 = p2[1] 
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    return Scalar(midx, midy, nR, x0, y0)

def Perimeter(aP, lComplete = False):
    points = [] 
    for i in aP:
        points += (i[0], i[1])
    if lComplete:
        points += (aP[0][0], aP[0][1])
    return points    

def linearTranslation(a1, points, r, a2):
    nL = len(points)
    p1 = array([a1] * nL, 'f')
    q = points - p1
    q = transpose(q)
    q = dot(r, q)
    q = transpose( q)
    p2 = array([a2] * nL, 'f')
    q = q + p2
    return q
       
class shape:
    def GetPoints(self):
        pass
    def __init__(self, cTag = None):
        if cTag == None:
            cTag = NewTag()
        self.length = [2,1,1,2]
        self.GetPoints()
        self.points   = array(self.points, 'f')
        self.vertices = self.points
        self.tag = cTag
    def draw(self):
        v = Perimeter(self.vertices)
        v.append(v[0])
        v.append(v[1])
        canvas.create_line(v, fill = 'orange', tag = self.tag, width = 1)
    def drawOutline(self, x, y, n0, nC):
        cosTheta = cos(n0)
        sinTheta = sin(n0)
        r     = array([[cosTheta, -sinTheta],[sinTheta,cosTheta]], 'f')
        q     = linearTranslation(self.points[nC], self.points, r, [x, y])
        self.vertices = q
        self.draw()
    def drawFill(self):
        points = Perimeter(self.vertices) 
        canvas.create_polygon(points, fill = self.colour, tag = self.tag)
    def drawComplete(self):
        self.drawFill()
        self.redArc()
        self.blueArc()
    def alignWith(self, nodeobj, nCnr2):
        p1 = nodeobj.p1 
        p2 = nodeobj.p2 
        dx1 = p2[0] - p1[0]
        dy1 = p2[1] - p1[1]
        nTheta2 = atan2(dy1,dx1)
        q1 = self.vertices[nCnr2]
        q2 = self.vertices[(nCnr2 - 1)%4]
        dx2 = q2[0] - q1[0]
        dy2 = q2[1] - q1[1]
        nTheta1 = atan2(dy2,dx2)
        self.drawOutline(p1[0], p1[1], nTheta2 - nTheta1,nCnr2)

class kite(shape):
    def GetPoints(self, cColour = 'brown'):
       self.points  = [[0,0]
                      ,[nSelfX,nSelfY]
                      ,[0,nScale * nFib]
                      ,[-nSelfX,nSelfY]]
       self.colour = cColour
       self.angles = [72,72,144,72]
       self.type   = 'kite'
        # shape, corner
       self.viable = [[[dart,1],[kite, 0]]
                     ,[[dart,2],[kite, 3]]
                     ,[[dart,3],[kite, 2]]
                     ,[[dart,0],[kite, 1]]]
    def draw(self):
        pass
    def redArc(self):
        nR = nRatioBig
        p0 = self.vertices[0]
        p1 = Scalar(self.vertices[3][0],self.vertices[3][1], nR, p0[0],p0[1])
        p5 = Scalar(self.vertices[1][0],self.vertices[1][1], nR, p0[0],p0[1])
        p3 = MidArc(p1,p5,p0,nR)
        p2 = MidArc(p1,p3,p0,nR)
        p4 = MidArc(p3,p5,p0,nR)
        aR = Perimeter([p1,p2,p3,p4,p5])
        canvas.create_line(aR, fill = 'darkgrey', tag = self.tag, width = 1)        
    def blueArc(self):
        nR = 1 / (1 / nFib + 1) * nScale
        p0 = self.vertices[2]
        p1 = Scalar(self.vertices[3][0],self.vertices[3][1], nR, p0[0],p0[1])
        p9 = Scalar(self.vertices[1][0],self.vertices[1][1], nR, p0[0],p0[1])
        p5 = MidArc(p1,p9,p0,nR)
        p3 = MidArc(p1,p5,p0,nR)
        p7 = MidArc(p5,p9,p0,nR)
        p2 = MidArc(p1,p3,p0,nR)
        p4 = MidArc(p3,p5,p0,nR)
        p6 = MidArc(p5,p7,p0,nR)
        p8 = MidArc(p7,p9,p0,nR)
        aR = Perimeter([p1,p2,p3,p4,p5,p6,p7,p8,p9])
        canvas.create_line(aR, fill = 'cyan', tag = self.tag, width = 1)
    def subShapes(self):
        subs = []
        p0 = list(self.vertices[0])
        p1 = list(self.vertices[1])
        p2 = list(self.vertices[2])
        p3 = list(self.vertices[3])
        p4 = Scalar(p3[0],p3[1], nRatioSmall, p0[0],p0[1])
        p5 = Scalar(p1[0],p1[1], nRatioSmall, p0[0],p0[1])
        p6 = Scalar(p2[0],p2[1], nRatioBig  , p0[0],p0[1])
        subs.append(SubKiteRight(p3,p6,p2))
        subs.append(SubKiteLeft(p3,p6,p4))
        subs.append(SubKiteRight(p1,p6,p5))
        subs.append(SubKiteLeft(p1,p6,p2))
        subs.append(SubDartRight(p6,p0,p5))
        subs.append(SubDartLeft(p6,p0,p4))
        return subs
    
class dart(shape):
    def GetPoints(self, cColour = 'darkgreen'):
        self.points = [[0,0]
               ,[nSelfX,nSelfY]
               ,[0,nScale] 
               ,[-nSelfX,nSelfY]]
        self.angles = [72,36,216,36]
        self.type   = 'dart'
        self.viable = [[[dart, 0],[kite, 1]]
                     ,[[kite, 2]]
                     ,[[kite, 3]]
                     ,[[dart, 1],[kite, 0]]] 
        self.colour = cColour
    def redArc(self):
        nR = nRatioSmall
        p0 = self.vertices[0]
        p1 = Scalar(self.vertices[3][0],self.vertices[3][1], nR, p0[0],p0[1])
        p5 = Scalar(self.vertices[1][0],self.vertices[1][1], nR, p0[0],p0[1])
        p3 = MidArc(p1,p5,p0,nR)
        p2 = MidArc(p1,p3,p0,nR)
        p4 = MidArc(p3,p5,p0,nR)
        aR = Perimeter([p1,p2,p3,p4,p5])
        canvas.create_line(aR, fill = 'darkgrey', tag = self.tag, width = 1)        
    def blueArc(self):
        nR = 1 / nFib / (1 / nFib + 1) * nScale
        p0 = self.vertices[2]
        p1 = Scalar(self.vertices[3][0],self.vertices[3][1], nR, p0[0],p0[1])
        p9 = Scalar(self.vertices[1][0],self.vertices[1][1], nR, p0[0],p0[1])
        p5 = MidArc(p1,p9,p0,nR)
        p5[0] = 2 * p0[0] - p5[0] # great arc
        p5[1] = 2 * p0[1] - p5[1] # great arc
        p3 = MidArc(p1,p5,p0,nR)
        p7 = MidArc(p5,p9,p0,nR)
        p2 = MidArc(p1,p3,p0,nR)
        p4 = MidArc(p3,p5,p0,nR)
        p6 = MidArc(p5,p7,p0,nR)
        p8 = MidArc(p7,p9,p0,nR)
        aR = Perimeter([p1,p2,p3,p4,p5,p6,p7,p8,p9])
        canvas.create_line(aR, fill = 'cyan', tag = self.tag, width = 1)        
    def subShapes(self):
        subs = []
        p0 = list(self.vertices[0])
        p1 = list(self.vertices[1])
        p2 = list(self.vertices[2])
        p3 = list(self.vertices[3])
        p4 = Scalar(p3[0],p3[1], nRatioBig, p0[0],p0[1])
        p5 = Scalar(p1[0],p1[1], nRatioBig, p0[0],p0[1])
        subs.append(SubKiteRight(p0,p2,p4))
        subs.append(SubKiteLeft(p0,p2,p5))
        subs.append(SubDartRight(p2,p3,p4))
        subs.append(SubDartLeft(p2,p1,p5))
        return subs

def AlterBorder(aBorder, temp, nNook, nAligned, nDel, nIns):
    cnr1 = nNook
    cnr2 = nAligned
    if nDel < 3:
        # replacement
        ang1 = aBorder[cnr1].angle    
        aBorder[cnr1]= NodeObject(temp, cnr2)
        aBorder[cnr1].angle = ang1
        aBorder[cnr1].prioritise()
    if cnr1 == len(aBorder) - 1:
        lClocked = True
    else:
        lClocked = False
    # deletion
    cnr3 =(cnr1 + 1) % len(aBorder)
    nAdjust = 1
    for z in range(nDel):
        if cnr3 < len(aBorder) - 1:
           aBorder = aBorder[:cnr3] + aBorder[cnr3 + 1:]
        elif cnr3 == len(aBorder): # delete first element
           aBorder = aBorder[1:]  
        else: # around the clock
           aBorder = aBorder[:cnr3]
    # insertion
    for nD in range(nIns):
        cnr4 = (cnr1 + nD + nAdjust) % len(aBorder)
        if lClocked:
            cnr4 = nD
        node = NodeObject(temp, (cnr2 + nD + 1) % 4)
        aBorder.insert(cnr4, node)
    return aBorder    

def FitsBorder(aBorder, nNook, aV, temp):
    nAligned = aV[1]
    nL = len(aBorder)
    for nBack in range(4):
        btest = aBorder[(nNook - nBack) % nL]
        angle1 = temp.angles[(nAligned + nBack) % 4]
        t = btest.angle - angle1
        if t < -nSmall: # conflict
            return False
        elif t > nSmall: # still room
            break
        # tight angle fit, test lengths
        nTestBorder = (nNook - nBack - 1) % nL
        nTestShape  = (nAligned + nBack) % 4
        btest       = aBorder[nTestBorder]
        if btest.length <> temp.length[nTestShape]: # length mismatch
            return False
    for nForward in range(4):
        btest = aBorder[(nNook + nForward + 1) % nL]
        angle1 = temp.angles[(nAligned - nForward - 1) % 4]
        t = btest.angle - angle1
        if t < -nSmall: # conflict
            return False
        elif t > nSmall: # still room
            break
        # tight angle fit, test lengths
        nTestBorder = (nNook + nForward + 1) % nL
        nTestShape  = (nAligned - nForward - 2) % 4
        btest       = aBorder[nTestBorder]
        if btest.length <> temp.length[nTestShape]: # length mismatch
            return False
    aBorder[nNook].nBack    = nBack
    aBorder[nNook].nForward = nForward
    return True



def addToBorder(aBorder, nNook, node, aV, AddTile):
    nAligned = aV[1]
    nL = len(aBorder)
    AddTile.alignWith(node, nAligned)
    nBack    = aBorder[ nNook].nBack
    nForward = aBorder[ nNook].nForward
    del aBorder[ nNook].nBack
    del aBorder[ nNook].nForward
    nTest    = (nNook - nBack) % nL
    btest    = aBorder[ nTest]
    nAlign   = (nAligned + nBack) % 4
    angle1   = AddTile.angles[nAlign]
    btest.angle -= angle1
    btest.prioritise() 
    btest       = aBorder[(nNook + nForward + 1) % nL]
    angle1      = AddTile.angles[(nAligned - nForward - 1) % 4]
    btest.angle -= angle1
    btest.prioritise()
    nDel = min(nForward + nBack, 3)
    nIns = max(2 - nDel, 0)
    aBorder = AlterBorder(aBorder, AddTile, nTest, nAlign, nDel, nIns)
    return aBorder


class NodeObject:
    def __init__(self, shape, edge):
        self.angle  = 360 - shape.angles[edge]
        self.length = shape.length[edge]
        self.p1     = shape.vertices[edge]
        self.p2     = shape.vertices[(edge + 1) % 4]
        self.edge   = edge
        self.x      = shape.vertices[edge][0]
        self.y      = shape.vertices[edge][1]
        self.dist   = sqrt((nW2 - self.x)**2 + (nH2 -self.y)**2)
        self.viable = shape.viable[edge]
        self.prioritise()
        self.shape = shape
    def prioritise(self):
        self.priority = self.angle + self.dist / nW 

def PauseMessage(cText):
    global lFinished
    lFinished = True
    canvas.create_text(nW/2,20,text = cText,fill = 'white', tag = 'pause')
    raw_input()
    canvas.delete('pause')    
               
def FillPlane(aBorder, level):
    # a small delay allows the screen to show
    print level, ' of ', nRecLim # when level gets too high the stack will overload
    if level >= nRecLim - 50:
        print 'The stack has maxed out!'
        PauseMessage('The initial pattern is complete, press ENTER to advance.')
        return {}
    aBorderCopy = deepcopy(aBorder)
    nMin = 10000
    k    = 'all filled'
    j    = k
    for i in aBorderCopy:
        if i.x <  nW * 0.05 or i.x > nW * 0.95: # dont go off the screen
            continue
        elif  i.y <  nH * 0.1 or i.y > nH * 0.9:
            continue
        elif i.priority < nMin:
            j = i
            nMin = i.priority
    aAdded = []
    # by choosing the most sensible place to add to
    # there is not such a need for conflict testing.
    if  j == k: # no more space to fill
        print 'complete'
        PauseMessage('The initial pattern is complete, press ENTER to advance.')
        return {}
    b = j
    i = aBorderCopy.index(b)
    viable = b.viable
    shuffle(viable)
    while len(viable) > 0:
        v = viable[0]
        viable = viable[1:]
        attempt = v[0]()
        if FitsBorder(aBorderCopy, i, v, attempt):
            aAdded.append(attempt.tag)
            aBorderCopy = addToBorder(aBorderCopy, i, b, v, attempt)
            oShapesDict = FillPlane(aBorderCopy, level + 1)
            for idtag in aAdded:
                canvas.delete(idtag)
            if lFinished:
                for n in aBorder:
                    oShapesDict[n.shape.tag] = n.shape
                return oShapesDict
            # it might be more efficient to do some sort of clean up
            # but this is eaisier
            aBorderCopy = deepcopy(aBorder)

class SubShape:
    def draw(self):    
        points = Perimeter(self.vertices) 
        canvas.create_polygon(points, fill = self.colour, tag = cDefTag)

class SubKiteRight(SubShape):
    def __init__(self,p0,p1,p2):
        self.vertices = deepcopy([p0,p1,p2])
        self.colour = 'beige'
    def subShapes(self):
        subs = []
        p0 = self.vertices[0]
        p1 = self.vertices[1]
        p2 = self.vertices[2]
        p3 = Scalar(p2[0],p2[1], nRatioSmall, p0[0],p0[1])
        p4 = Scalar(p1[0],p1[1], nRatioBig  , p0[0],p0[1])
        subs.append(SubKiteRight(p2,p4,p1))
        subs.append(SubKiteLeft(p2,p4,p3))
        subs.append(SubDartLeft(p4,p0,p3))
        return subs
        
class SubKiteLeft(SubShape):
    global lAlternate
    def __init__(self,p0,p1,p2):
        self.vertices = deepcopy([p0,p1,p2])
        self.colour = 'tan'            

    def subShapes(self):        
        subs = []
        p0 = self.vertices[0]
        p1 = self.vertices[1]
        p2 = self.vertices[2]
        p3 = Scalar(p2[0],p2[1], nRatioSmall, p0[0],p0[1])
        p4 = Scalar(p1[0],p1[1], nRatioBig  , p0[0],p0[1])
        subs.append(SubKiteRight(p2,p4,p3))
        subs.append(SubKiteLeft(p2,p4,p1))
        subs.append(SubDartRight(p4,p0,p3))
        return subs

class SubDartRight(SubShape):
    def __init__(self,p0,p1,p2):
        self.vertices = deepcopy([p0,p1,p2])
        self.colour = 'darkgrey'            
        
    def subShapes(self):
        subs = []
        p0 = self.vertices[0]
        p1 = self.vertices[1]
        p2 = self.vertices[2]
        p3 = Scalar(p1[0],p1[1], nRatioSmall, p0[0],p0[1])
        subs.append(SubKiteRight(p1,p2,p3))
        subs.append(SubDartRight(p2,p0,p3))
        return subs
class SubDartLeft(SubShape):        
    def __init__(self,p0,p1,p2):
        self.vertices = deepcopy([p0,p1,p2])
        self.colour = 'grey'
        
    def subShapes(self):
        subs = []
        p0 = self.vertices[0]
        p1 = self.vertices[1]
        p2 = self.vertices[2]
        p3 = Scalar(p1[0],p1[1], nRatioSmall, p0[0],p0[1])
        subs.append(SubKiteLeft(p1,p2,p3))
        subs.append(SubDartLeft(p2,p0,p3))
        return subs

seed()
aBorder = []
lFinished = False
if random() > 0.5:
   temp = kite('first')
else:
   temp = dart('first')
temp.drawOutline(nW2, nH2, 0, 0)
for i in range(4):
    aBorder.append(NodeObject(temp, i))
oShapesDict = FillPlane(aBorder, 1)
canvas.delete('first')
cDefTag = NewTag()
aSubShapes  = []
for s in oShapesDict:
    print '#'
    oShape = oShapesDict[s]
    oShape.drawComplete()
    aSubShapes += oShape.subShapes()

while True:
    nRatioSmall *= nFib / (nFib + 1)
    nRatioBig   *= nFib / (nFib + 1)
    PauseMessage('press ENTER again to "DEFLATE" the pattern.')
    cLastTag = cDefTag
    cDefTag  = NewTag()
    aNewSubs = []
    for s in aSubShapes:
        s.draw()
        print '#'
        t = s.subShapes()
        aNewSubs += t
    canvas.delete(cLastTag)        
    lAlternate = True    
    aSubShapes = deepcopy(aNewSubs)
