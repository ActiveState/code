''' This program uses the stepping stone algorithum to solve
the transhipment problem. That is how to transport various quuantities
of material to various destinations minimising overall cost, given
the various costs of sending a unit from each source to each destination.
The sum of supply and demand must equal.'''

def PrintOut():
    GetDual()
    nCost = 0
    print
    print '    DEMAND' + ' ' * ( m * 10) + 'SUPPLY'
    for y in aDemand:    
        print '%10i' % y,
    print    
    for x in range( n):
        for y in range( m):
            nCost += aCost[ x][ y] * aRoute[ x][ y]
            if aRoute[ x][ y] == 0:
                print '[<%2i>%4i]' %( aCost[ x][ y], aDual[ x][ y]),
            else:
                print '[<%2i>(%2i)]' %( aCost[ x][ y], aRoute[ x][ y] + 0.5),
        print ' : %i' % aSupply[ x]
    print 'Cost: ', nCost
    print 'Press ENTER to continue'
    raw_input()
        
def NorthWest():
    ''' The simplest method to get an initial solution.
    Not the most efficient'''
    global aRoute
    u  = 0
    v  = 0
    aS = [ 0] * m
    aD = [ 0] * n
    while u <= n - 1 and v <= m - 1:
        if aDemand[ v] - aS[ v] < aSupply[ u] - aD[ u]:
            z              = aDemand[ v] - aS[ v]
            aRoute[ u][ v] = z
            aS[ v]        += z
            aD[ u]        += z
            v             += 1
        else:
            z              = aSupply[ u] - aD[ u]
            aRoute[ u][ v] = z
            aS[ v]        += z
            aD[ u]        += z
            u             += 1

def NotOptimal():
    global PivotN
    global PivotM
    nMax = -nVeryLargeNumber
    GetDual()
    for u in range( 0, n):
        for v in range( 0, m):
            x = aDual[ u][ v]
            if x > nMax:
                nMax = x
                PivotN = u
                PivotM = v
    return ( nMax > 0)

def GetDual():
    global aDual
    for u in range( 0, n):
        for v in range( 0, m):
            aDual[ u][ v] = -0.5 # null value
            if aRoute[ u][ v] == 0:
                aPath = FindPath( u, v)
                z     = -1
                x     = 0
                for w in aPath:
                    x += z * aCost[ w[ 0]][ w[ 1]]
                    z *= -1
                aDual[ u][ v] = x
                
def FindPath( u, v):
    aPath = [[ u, v]]
    if not LookHorizontaly( aPath, u, v, u, v):
        print 'Path error, press key', u, v
        raw_input()
    return aPath

def LookHorizontaly( aPath, u, v, u1, v1):
    for i in range( 0, m):
        if i != v and aRoute[ u][ i] != 0:
            if i == v1:
                aPath.append( [ u, i])
                return True # complete circuit
            if LookVerticaly( aPath, u, i, u1, v1):
                aPath.append( [ u, i])
                return True
    return False # not found

def LookVerticaly( aPath, u, v, u1, v1):
    for i in range( 0, n):
        if i != u and aRoute[ i][ v] != 0:
            if LookHorizontaly( aPath, i, v, u1, v1):
                aPath.append([ i, v])
                return True
    return False # not found

def BetterOptimal():
    global aRoute
    aPath = FindPath( PivotN, PivotM)
    nMin  = nVeryLargeNumber
    for w in range( 1, len( aPath), 2):
        t = aRoute[ aPath[ w][ 0]][ aPath[ w][ 1]]
        if t < nMin:
            nMin = t
    for w in range( 1 , len( aPath), 2):
        aRoute[ aPath[ w][ 0]][ aPath[ w][ 1]]         -= nMin
        aRoute[ aPath[ w - 1][ 0]][ aPath[ w - 1][ 1]] += nMin

# example 1
aCost = [[ 2, 1, 3, 3, 2, 5]
        ,[ 3, 2, 2, 4, 3, 4]
        ,[ 3, 5, 4, 2, 4, 1]
        ,[ 4, 2, 2, 1, 2, 2]]

aDemand = [ 30, 50, 20, 40, 30, 11]
aSupply = [ 50, 40, 60, 31]

''' example 2
aCost = [[ 1, 2, 1, 4, 5, 2]
        ,[ 3, 3, 2, 1, 4, 3]
        ,[ 4, 2, 5, 9, 6, 2]
        ,[ 3, 1, 7, 3, 4, 6]]
aDemand = [ 20, 40, 30, 10, 50, 25]
aSupply = [ 30, 50, 75, 20]
'''
''' example3
aCost = [[ 5, 3, 6, 2]
        ,[ 4, 7, 9, 1]
        ,[ 3, 4, 7, 5]]
aDemand = [ 16, 18, 30, 25]
aSupply = [ 19, 37, 34]         
'''         
n = len( aSupply)
m = len( aDemand)
nVeryLargeNumber = 99999999999
# add a small amount to prevent degeneracy
# degeneracy can occur when the sums of subsets of supply and demand equal
elipsis = 0.001
for k in aDemand:
    k += elipsis / len( aDemand)
aSupply[ 1] += elipsis
# initialisation
aRoute = []
for x in range( n):
    aRoute.append( [ 0] * m)
aDual  = []
for x in range( n):
    aDual.append( [ -1] * m)
NorthWest()
PivotN = -1
PivotM = -1
PrintOut()
# MAIN
while NotOptimal():
    print 'PIVOTING ON', PivotN, PivotM
    BetterOptimal()
    PrintOut()
print "FINISHED"
