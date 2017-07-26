# Author: James Collins
# Program to generate a fractal planet. ( blobby planet).
# It expands a platonic solid into a geodetic sphere.
# Then draws a projection of said sphere ( mercator projection).
# The print statements have been left in for debugging
# The program will run a little faster without them
# Big O is exponential w.r.t repeatTimes
# If too slow reduce the variable 'repeatTimes' below
repeatTimes = 4 # NUMBER OF CYCLES

from Tkinter import *
from winsound import Beep
from math import *
from random import*
from time import *

W = 800  # canvas dimensions
H = 600  # adjust to suit
scale = 200
def FindRef( crossRef, p, q):
    a = min( p, q) 
    b = max( p, q)
    faceKey = str( a) + ':' + str( b)
    return crossRef[ faceKey]

def ColStr( x):
    if x > 255:
        x = 0
    if x < 0:
        x = 255
    s = "%x" % x # converts x into a hexidecimal string
    if len( s) < 2:
        s = '0' + s
    return s

def AddIfUnique( NewEdges, edge):
    a = edge[ 0]
    b = edge[ 1]
    if a > b:
        a, b = b, a
        edge[ 0] = a
        edge[ 1] = b
    faceKey = str( a) + ':' + str( b)
    if not NewEdges.has_key( faceKey):
        c = edge[ 2]
        d = edge[ 3]
        NewEdges[ faceKey] = [ a, b, c, d]
    return NewEdges

def AddIfFaceUnique( faces, x1, y1, z1, x2, y2, z2, x3, y3, z3, C, p, q, r, scale, H):
    if p > q:
        p, q = q, p
    if p > r:
        p, r = r, p
    if q > r:
        q, r = r, q
    faceKey = str( p) + ':' + str( q) + ':' + str( r)
    if not faces.has_key( faceKey):
       faces[ faceKey] = [ x1, y1, z1, x2, y2, z2, x3, y3, z3, C]
    return faces

def ConvertTo255( x):
    """
    The color scheme has been chosen to create a typical
    earthlike or M class , planet.
    """
    x = x / abs( x) * 3 * sqrt( abs( x / 3))
    if x > 0:
        x /= 1.5
    if x > 2.5:
        return 'white'
    if x < -0.6: # blues
        return '#0000' + ColStr( int( random() * 55) + 200)
    if x < -0.2: # -0.6 to -0.2 cyan colours
        x = int(( -x - 0.6) / 0.4 * 127) + 127
        return '#50' + ColStr( int( x / 2) + 30) + ColStr( 255 - x)
    if x > 1.7: # grey colours 1.7 - 2.5
        x = int(( x - 1.7) / 0.8 * 127) + 127
        return '#' + ColStr( x) + ColStr( x) + ColStr( x)
    if x > 1.5: # brown colours 1.5 - 1.7
        x = int(( x - 1.5) / 0.2 * 120 / 2)  + 120
        return '#' + ColStr( x + 30) + ColStr( x - 30) + ColStr( x - 30)
    if x > 1.0: # kaki colours 0.8 - 1.3
        z = 1 - ( x - 0.8) / 0.7
        x = 150 - int( z * 60)
        y = 190 + int( z * 20)
        z = 100 - int( z * 30)
        return '#' + ColStr( x) + ColStr( y) + ColStr( z)
    else: # green colours -0.2 - 1.0
        x = int(( x - 0.2) / 1.6 * 60) + 120
        return '#20' + ColStr( x + 60) + ColStr( x)

def SphericalCoords( x, y, z, W2, H2):
    r = sqrt( x * x + y * y)
    alpha = atan2( y , x) * W2 / pi  * 0.95 + W2 
    beta  = atan2( z , r) * H2 / pi * 2 * 0.95 + H2
    return alpha, beta

def DrawShape(  edges, vertex):
    Beep( 100, 100)
    angle = 0
    nAverage = 0
    for i in vertex:
        nAverage += i[ 3]
    nAverage = nAverage / len( vertex)
    nVar = 0
    for i in vertex:
        nVar = nVar + ( i[ 3] - nAverage)**2
    nStandardDeviation = sqrt( nVar / (len( vertex) - 1))
    lene = int( len( edges) / 100)
    counte = 0
    faces  = {}
    edgeKeys = edges.keys()
    for i in edgeKeys:
        counte += 1
        if counte > lene:
            print '$',
            counte = 0
        edge = edges[ i]
        p  = edge[ 0]
        q  = edge[ 1]
        l  = edge[ 2]
        r  = edge[ 3]
        x1 = vertex[ p][ 0] 
        y1 = vertex[ p][ 1] * scale + H/2
        z1 = vertex[ p][ 2] 
        r1 = vertex[ p][ 3]
        x2 = vertex[ q][ 0] 
        y2 = vertex[ q][ 1] * scale + H/2 
        z2 = vertex[ q][ 2] 
        r2 = vertex[ q][ 3]
        x3 = vertex[ l][ 0] 
        y3 = vertex[ l][ 1] * scale + H/2 
        z3 = vertex[ l][ 2] 
        r3 = vertex[ l][ 3]
        x4 = vertex[ r][ 0] 
        y4 = vertex[ r][ 1] * scale + H/2 
        z4 = vertex[ r][ 2] 
        r4 = vertex[ r][ 3]
        r1 = (r1 + r2 + r3)/3
        r2 = (r1 + r2 + r4)/3
        C1 = ConvertTo255(( r1 - nAverage) / nStandardDeviation )
        C2 = ConvertTo255(( r2 - nAverage) / nStandardDeviation)
        faces = AddIfFaceUnique( faces, x1, y1, z1, x2, y2, z2, x3, y3, z3, C1, p, q, l, scale, H)
        faces = AddIfFaceUnique( faces, x1, y1, z1, x2, y2, z2, x4, y4, z4, C2, p, q, r, scale, H)
    fK = faces.keys()
    canvas = Canvas( width = W, height = H)
    canvas.pack(side = TOP)
    Beep( 200, 100)
    #draws spinning globe
    canvas.create_rectangle( 0, 0, W, H, fill = 'black', width = 0, tag ='o')
    angle = 0
    while angle < pi * 2:
        shotTime = time()
        angle += 30 * pi / 180
        cosAngle = cos( angle)
        sinAngle = sin( angle)
        W2 = W / 2
        for i in fK:
            fList = faces[ i]
            x1 = fList[ 0] 
            y1 = fList[ 1] 
            z1 = fList[ 2]
            x2 = fList[ 3] 
            y2 = fList[ 4] 
            z2 = fList[ 5] 
            x3 = fList[ 6] 
            y3 = fList[ 7] 
            z3 = fList[ 8] 
            C1 = fList[ 9]
            u1 = cosAngle * x1 + sinAngle * z1
            v1 = cosAngle * z1 - sinAngle * x1
            u2 = cosAngle * x2 + sinAngle * z2
            v2 = cosAngle * z2 - sinAngle * x2
            u3 = cosAngle * x3 + sinAngle * z3
            v3 = cosAngle * z3 - sinAngle * x3
            if v1 + v2 + v3 >= 0:
                u1 = u1 * scale + W2
                u2 = u2 * scale + W2
                u3 = u3 * scale + W2
                canvas.create_polygon( u1, y1, u2, y2, u3, y3, fill = C1, tag = 'x')
                #canvas.create_line( u1, y1, u2, y2, u3, y3, u1, y1, fill = 'black', tag = 'x')
        canvas.update()
        while time() - shotTime < 0.2:
            sleep( 1)
        canvas.delete( 'x')
    Beep( 200, 100)
    # draws flat map
    canvas.create_rectangle( 0, 0, W, H, fill = 'black', width = 0, tag ='o')
    W2 = W / 2
    H2 = H / 2
    W34 = W * 3 / 4
    W4  = W / 4 
    Ws  = W * 0.95
    for i in fK:
        fList = faces[ i]
        x1 = fList[ 0] 
        y1 = ( fList[ 1] - H2)/ scale 
        z1 = fList[ 2]
        x2 = fList[ 3] 
        y2 = ( fList[ 4] - H2)/ scale 
        z2 = fList[ 5] 
        x3 = fList[ 6] 
        y3 = ( fList[ 7] - H2)/ scale 
        z3 = fList[ 8] 
        C1 = fList[ 9]
        u1 ,v1 = SphericalCoords( x1, y1, z1, W2, H2)
        u2 ,v2 = SphericalCoords( x2, y2, z2, W2, H2)
        u3 ,v3 = SphericalCoords( x3, y3, z3, W2, H2)
        if u1 > W34:
            if u2 < W4 or u3 < W4:
                u1 -= Ws
        if u2 > W34:
           if u1 < W4 or u3 < W4:
                u2 -= Ws
        if u3 > W34:
            if u2 < W4 or u1 < W4:
                u3 -= Ws
        canvas.create_polygon( u1, v1, u2, v2, u3, v3, fill = C1, tag = 'x')
        #canvas.create_line( u1, v1, u2, v2, u3, v3, u1, v1, fill = 'black', tag = 'x')
    canvas.update()
        

# icosahedron
"""
using other platonic solids gives
a slightly different flavour to your planet.
"""

t = ( sqrt( 5.0) - 1) / 2
# x, y, z, altitude
vertex = [[   0, 1, t,1]
          ,[  0, 1,-t,1]
          ,[  1, t, 0,1]
          ,[  1,-t, 0,1]
          ,[  0,-1,-t,1]
          ,[  0,-1, t,1]
          ,[  t, 0, 1,1]
          ,[ -t, 0, 1,1]
          ,[  t, 0,-1,1]
          ,[ -t, 0,-1,1]
          ,[ -1, t, 0,1]
          ,[ -1,-t, 0,1]]
# start point, end point, left hand path point, right hand path point
edges2 =[[0, 1, 2, 10]
        , [0, 2, 1, 6]
        , [0, 6, 2, 7]
        , [0, 7, 6, 10]
        , [0, 10, 1, 7]
        , [1, 2, 0, 8]
        , [1, 8, 2, 9]
        , [1, 9, 8, 10]
        , [1, 10, 0, 9]
        , [2, 8, 3, 1]
        , [2, 3, 6, 8]
        , [2, 6, 0, 3]
        , [3, 8, 2, 4]
        , [3, 4, 5, 8]
        , [3, 5, 4, 6]
        , [3, 6, 2, 5]
        , [4, 8, 3, 9]
        , [4, 9, 8, 11]
        , [4, 11, 5, 9]
        , [4, 5, 3, 11]
        , [5, 6, 3, 7]
        , [5, 7, 6, 11]
        , [5, 11, 7, 4]
        , [6, 7, 0, 5]
        , [7, 10, 0, 11]
        , [7, 11, 5, 10]
        , [8, 9, 1, 4]
        , [9, 10, 1, 11]
        , [9, 11, 4, 10]
        , [10, 11, 9, 7]]
seed()
count = 0
edges = {}
for i in edges2:
        edges = AddIfUnique( edges, i)
for i in vertex:
    x1 = i[ 0]
    y1 = i[ 1]
    z1 = i[ 2]
    r3 = sqrt( x1 * x1 + y1 * y1 + z1 * z1)
    i[ 3] = r3
scaleFactor = 1.0/100 * r3
timer = time()
lastTime = 1
for count in xrange( repeatTimes): 
    print count , 'of ' , repeatTimes - 1
    crossRef = {}
    lene = int( len( edges) / 100)
    counte = 0
    edgeKeys = edges.keys()
    for i in edgeKeys:
        counte += 1
        if counte > lene:
            print '#',
            counte = 0
        edge = edges[ i]    
        a = edge[ 0]
        b = edge[ 1]
        x1 = vertex[ a][ 0]
        y1 = vertex[ a][ 1]
        z1 = vertex[ a][ 2]
        x2 = vertex[ b][ 0]
        y2 = vertex[ b][ 1]
        z2 = vertex[ b][ 2]
        r3 = vertex[ a][ 3]
        r4 = vertex[ b][ 3]
        # normal distribution , scale invariant , to calculate altitude  
        r = ( r3 + r4)/ 2 + ( random() + random() + random() - 1.5) * scaleFactor
        x = x1 + x2
        y = y1 + y2        
        z = z1 + z2
        r2 = sqrt( x * x + y * y + z * z)
        r2 = r2 / r
        x  = x / r2
        y  = y / r2
        z  = z / r2
        vertex.append( [ x, y, z, r])
        n = len( vertex) - 1
        crossRef[ str( min( a, b)) + ':' + str( max( a, b))] = n
    NewEdges = {}
    lene = int( len( crossRef) / 100)
    print
    counte = 0
    counte2 = 0
    lene = int( len( edges) / 100)
    for i in edgeKeys:
        counte += 1
        if counte > lene:
            counte2 += 1
            print counte2,
            counte = 0
        edge = edges[ i]    
        p = edge[ 0] # start
        q = edge[ 1] # end
        l = edge[ 2] # outer left
        r = edge[ 3] # outer right
        x = FindRef( crossRef, p, q) # new intermediary points
        y = FindRef( crossRef, p, l)
        z = FindRef( crossRef, q, l)
        v = FindRef( crossRef, q, r)
        w = FindRef( crossRef, p, r)
        NewEdges = AddIfUnique( NewEdges, [ p, x, y, w])
        NewEdges = AddIfUnique( NewEdges, [ q, x, v, z])        
        NewEdges = AddIfUnique( NewEdges, [ w, x, p, v])
        NewEdges = AddIfUnique( NewEdges, [ y, x, p, z])    
        NewEdges = AddIfUnique( NewEdges, [ z, x, q, y])    
        NewEdges = AddIfUnique( NewEdges, [ v, x, q, w])    
    edges = NewEdges
    scaleFactor = scaleFactor / 2 # each edge halved
    timer2 = time()
    thisTime = timer2 - timer
    print
    print 'time taken', thisTime
    print 'memory', len( vertex), len( edges)
    print 'time ratio = ', thisTime / lastTime
    print 'expectedTime to finish = ', round( thisTime * ( thisTime / lastTime) ** ( repeatTimes - count - 1) / 60, 2), ' minutes'
    lastTime = thisTime
    timer = time()
print 'PREPARING TO DRAW SHAPE'    
DrawShape( edges, vertex)
