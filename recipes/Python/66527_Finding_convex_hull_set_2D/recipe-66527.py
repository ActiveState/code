#!/usr/bin/env python

"""convexhull.py

Calculate the convex hull of a set of n 2D-points in O(n log n) time.  
Taken from Berg et al., Computational Geometry, Springer-Verlag, 1997.
Prints output as EPS file.

When run from the command line it generates a random set of points
inside a square of given length and finds the convex hull for those,
printing the result as an EPS file.

Usage:

    convexhull.py <numPoints> <squareLength> <outFile>

Dinu C. Gherman
"""


import sys, string, random


######################################################################
# Helpers
######################################################################

def _myDet(p, q, r):
    """Calc. determinant of a special matrix with three 2D points.

    The sign, "-" or "+", determines the side, right or left,
    respectivly, on which the point r lies, when measured against
    a directed vector from p to q.
    """

    # We use Sarrus' Rule to calculate the determinant.
    # (could also use the Numeric package...)
    sum1 = q[0]*r[1] + p[0]*q[1] + r[0]*p[1]
    sum2 = q[0]*p[1] + r[0]*q[1] + p[0]*r[1]

    return sum1 - sum2


def _isRightTurn((p, q, r)):
    "Do the vectors pq:qr form a right turn, or not?"

    assert p != q and q != r and p != r
            
    if _myDet(p, q, r) < 0:
	return 1
    else:
        return 0


def _isPointInPolygon(r, P):
    "Is point r inside a given polygon P?"

    # We assume the polygon is a list of points, listed clockwise!
    for i in xrange(len(P[:-1])):
        p, q = P[i], P[i+1]
        if not _isRightTurn((p, q, r)):
            return 0 # Out!        

    return 1 # It's within!


def _makeRandomData(numPoints=10, sqrLength=100, addCornerPoints=0):
    "Generate a list of random points within a square."
    
    # Fill a square with random points.
    min, max = 0, sqrLength
    P = []
    for i in xrange(numPoints):
	rand = random.randint
	x = rand(min+1, max-1)
	y = rand(min+1, max-1)
	P.append((x, y))

    # Add some "outmost" corner points.
    if addCornerPoints != 0:
	P = P + [(min, min), (max, max), (min, max), (max, min)]

    return P


######################################################################
# Output
######################################################################

epsHeader = """%%!PS-Adobe-2.0 EPSF-2.0
%%%%BoundingBox: %d %d %d %d

/r 2 def                %% radius

/circle                 %% circle, x, y, r --> -
{
    0 360 arc           %% draw circle
} def

/cross                  %% cross, x, y --> -
{
    0 360 arc           %% draw cross hair
} def

1 setlinewidth          %% thin line
newpath                 %% open page
0 setgray               %% black color

"""

def saveAsEps(P, H, boxSize, path):
    "Save some points and their convex hull into an EPS file."
    
    # Save header.
    f = open(path, 'w')
    f.write(epsHeader % (0, 0, boxSize, boxSize))

    format = "%3d %3d"

    # Save the convex hull as a connected path.
    if H:
        f.write("%s moveto\n" % format % H[0])
        for p in H:
            f.write("%s lineto\n" % format % p)
        f.write("%s lineto\n" % format % H[0])
        f.write("stroke\n\n")

    # Save the whole list of points as individual dots.
    for p in P:
        f.write("%s r circle\n" % format % p)
        f.write("stroke\n")
            
    # Save footer.
    f.write("\nshowpage\n")


######################################################################
# Public interface
######################################################################

def convexHull(P):
    "Calculate the convex hull of a set of points."

    # Get a local list copy of the points and sort them lexically.
    points = map(None, P)
    points.sort()

    # Build upper half of the hull.
    upper = [points[0], points[1]]
    for p in points[2:]:
	upper.append(p)
	while len(upper) > 2 and not _isRightTurn(upper[-3:]):
	    del upper[-2]

    # Build lower half of the hull.
    points.reverse()
    lower = [points[0], points[1]]
    for p in points[2:]:
	lower.append(p)
	while len(lower) > 2 and not _isRightTurn(lower[-3:]):
	    del lower[-2]

    # Remove duplicates.
    del lower[0]
    del lower[-1]

    # Concatenate both halfs and return.
    return tuple(upper + lower)


######################################################################
# Test
######################################################################

def test():
    a = 200
    p = _makeRandomData(30, a, 0)
    c = convexHull(p)
    saveAsEps(p, c, a, file)


######################################################################

if __name__ == '__main__':
    try:
        numPoints = string.atoi(sys.argv[1])
        squareLength = string.atoi(sys.argv[2])
        path = sys.argv[3]
    except IndexError:
        numPoints = 30
        squareLength = 200
        path = "sample.eps"

    p = _makeRandomData(numPoints, squareLength, addCornerPoints=0)
    c = convexHull(p)
    saveAsEps(p, c, squareLength, path)
