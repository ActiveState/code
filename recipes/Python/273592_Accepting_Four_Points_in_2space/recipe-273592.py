from sets import Set

class onePoint :
    def __init__ ( self, X, Y ) :
        self . x = X
        self . y = Y
        
    def __repr__ ( self ) :
        return 'onePoint ( %s, %s )' % ( self . x, self . y )

def DistanceSq ( P0, P1 ) :
    
    return ( P0 . x - P1 . x ) ** 2 + ( P0 . y - P1 . y ) ** 2
        
class FourCorners :
    """http://www.mathpages.com/home/kmath201.htm:
    ... area of the ... triangle

            (x2-x3)(y1-y2) - (x1-x2)(y2-y3)
      A  =  -------------------------------
                           2

    
        In this same way it's easy to deduce that the area enclosed by a
    general quadralateral can be expressed in terms of the coordinates
    of its verticies as
    
           (x2-x4)(y1-y3) - (x1-x3)(y2-y4)
     A  =  -------------------------------
                          2
    
           1  /                                                     \
        =  - ( (x2y1-x1y2) + (x3y2-x2y3) + (x4y3-x3y4) + (x1y4-x4y1) )
           2  \                                                     /
    
    It's worth noting that, assuming all the verticies are in the ++
    quadrant of the xy coordinate system (i.e., all the coordinates are
    positive), these formulas give the positive area only if the verticies
    are numbered clockwise around the perimeter.  If they are counter-
    clockwise, the computed area is negative.  Of course, a quadralateral
    can have crossing edges, such that the verticies are clockwise around
    one region and counter-clockwise around the other.  Thus, the computed
    area of a non-degenerate quadralateral can vanish, as in the case of
    the quadralateral shown in Figure 3.
    """
    def __init__ ( self, alignmentImageSize, originalImageSize ) :
        self . _four = [ ]
        self . alignmentImageSize = alignmentImageSize 
        self . originalImageSize = originalImageSize
    
    def buildResult ( self, status ) :
        pointsCriterion = PointsCriterion ( * self . _four )
        result = { }
        for item in self . __dict__ :
            result [ item ] = self . __dict__ [ item ]
            
        for item in pointsCriterion . __dict__ :
            result [ item ] = pointsCriterion . __dict__ [ item ]
            
        result [ 'number' ] = len ( self . _four )
        
        return result
            
    def send ( self, pointTuple ) :
        
        point = onePoint ( * pointTuple )
        for aFour in self . _four :
            if aFour . x == point . x and aFour . y == point . y :
                if len ( self . _four ) < 4 :
                    return { 'number': len ( self . _four ), 'status': "Duplicate point (rejected)", }
                else :
                    return self . buildResult ( "Duplicate point (rejected)" )
        if len ( self . _four ) == 4 :
            distances = { }
            for aFour in self . _four :
                distances [ DistanceSq ( aFour, point ) ] = aFour
            self . _four . remove ( distances [ min ( distances ) ] )
        self . _four . append ( point )
        if len ( self . _four ) < 4 :
            return { 'number': len ( self . _four ), 'status': "Need four distinct points", }
        return self . buildResult ( 'Have four points' )

class PointsCriterion :

    def QuadrilateralAreaAux ( self, P0, P1, P2, P3 ) :
        return 0.5 * ( ( P1 . x - P3 . x ) * ( P0 . y - P2 . y ) - ( P0 . x - P2 . x ) * ( P1 . y - P3 . y ) )

    def TriangleAreaAux ( self, P0, P1, P2 ) :
        return 0.5 * ( ( P1 . x - P2 . x ) * ( P0 . y - P1 . y ) - ( P0 . x - P1 . x ) * ( P1 . y - P2 . y ) )
    
    def __init__  ( self, P0, P1, P2, P3 ) :

        areas = { }
        tours = [ [ 0, 1, 2, 3 ], [ 0, 1, 3, 2 ], [ 0, 2, 1, 3 ], [ 0, 3, 1, 2 ], ]
        points = [ P0, P1, P2, P3 ]
        for tour in tours :
            area = self . QuadrilateralAreaAux ( * tuple ( [ points [ t ] for t in tour ] ) )
            if area :
                if area < 0 :
                    tour . reverse ( )
                areas [ abs ( area ) ] = tour 
        area = max ( areas )
        
        clockwiseCorners = areas [ area ]
        comparisonArea = 2. * self . TriangleAreaAux ( * tuple ( [ points [ t ] for t in clockwiseCorners [ : 3 ] ] ) )
            
        corners = [ points [ p ] for  p in clockwiseCorners ]
        
        horizontals = [ corner . x for corner in corners ]
        horizontals . sort ( )
        
        verticals = [ corner . y for corner in corners ]
        verticals . sort ( )
        
        lefts = Set ( [ corner for corner in corners if corner . x in horizontals [ : 2 ] ] )
        rights = Set ( [ corner for corner in corners if corner . x in horizontals [ -2 : ] ] )
            
        uppers = Set ( [ corner for corner in corners if corner . y in verticals [ : 2 ] ] )
        lowers = Set ( [ corner for corner in corners if corner . y in verticals [ -2 : ] ] )
            
        self . upperLeft = lefts . intersection ( uppers ) . pop ( )
        self . lowerLeft = lefts . intersection ( lowers ) . pop ( )
        self . upperRight = rights . intersection ( uppers ) . pop ( )
        self . lowerRight = rights . intersection ( lowers ) . pop ( )
        
        self . horizontalRacking = self . lowerLeft . x - self . upperLeft . x
        self . verticalRacking = self . upperRight . y - self . upperLeft . y
        
        self . upperMost = min ( [ P . y for P in corners ] )
        self . leftMost = min ( [ P . x for P in corners ] )
        self . rightMost = max ( [ P . x for P in corners ] )
        self . lowerMost = max ( [ P . y for P in corners ] )
        
        self . quality = area / comparisonArea
        self . corners = corners

if __name__ == "__main__" :
    fourCorners = FourCorners ( ( 110, 110 ), ( 500, 500 ) )
    for corner in [ ( 0, 0 ), ( 0, 0 ), ( 100, 100 ), ( 0, 100 ), ( 0, 100 ), ( 100, 0 ), ( 5, 0 ), ( 100, 0 ), ( 100, 120 ), ( 100, 101 ), ( 100, 0 ), ] :
        result = fourCorners . send ( corner )
        for item in result :
            print item, result [ item ]
        print 100 * '='
