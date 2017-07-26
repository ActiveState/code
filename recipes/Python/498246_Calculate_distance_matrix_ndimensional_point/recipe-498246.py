from scipy import reshape, sqrt, identity

# nDimPoints: list of n-dim tuples
# distFunc: calculates the distance based on the differences
# Ex: Manhatten would be: distFunc=sum(deltaPoint[d] for d in xrange(len(deltaPoint)
def calcDistanceMatrix(nDimPoints, 
                       distFunc=lambda deltaPoint: sqrt(sum(deltaPoint[d]**2 for d in xrange(len(deltaPoint))))):
    nDimPoints = array(nDimPoints)
    dim = len(nDimPoints[0])
    delta = [None]*dim
    for d in xrange(dim):
        data = nDimPoints[:,d]
        delta[d] = data - reshape(data,(len(data),1)) # computes all possible combinations

    dist = distFunc(delta)
    dist = dist + identity(len(data))*dist.max() # eliminate self matching
    # dist is the matrix of distances from one coordinate to any other
    return dist

from numpy.matlib import repmat, repeat
def calcDistanceMatrixFastEuclidean(points):
    numPoints = len(points)
    distMat = sqrt(sum((repmat(points, numPoints, 1) - repeat(points, numPoints, axis=0))**2, axis=1))
    return distMat.reshape((numPoints,numPoints))

from numpy import mat, zeros, newaxis
def calcDistanceMatrixFastEuclidean2(nDimPoints):
    nDimPoints = array(nDimPoints)
    n,m = nDimPoints.shape
    delta = zeros((n,n),'d')
    for d in xrange(m):
        data = nDimPoints[:,d]
        delta += (data - data[:,newaxis])**2
    return sqrt(delta)

#################
# Unittest
#################
class CalcDistanceMatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.distanceMatrixFunc = "calcDistanceMatrix"
    
    def test_2D(self):
        points = [[0, 0], [1, 1], [4, 5]]
        dm = eval("%s(points)"%self.distanceMatrixFunc)
        self.assertAlmostEqual(1.414213562373095049, dm[0][1])
        self.assertAlmostEqual(6.403124237432848686, dm[0][2])
        self.assertAlmostEqual(5, dm[1][2])
        self._testSymmetry(dm)
        
    def test_3D(self):
        points = [[0, 0, 0], [1.0, 1, 1], [4, 5, 6], [10,10,10]]
        dm = eval("%s(points)"%self.distanceMatrixFunc)
        self.assertAlmostEqual(1.732050807568877294, dm[0][1])
        self.assertAlmostEqual(8.77496438739212206, dm[0][2])
        self.assertAlmostEqual(17.32050807568877294, dm[0][3])
        self.assertAlmostEqual(7.071067811865475244, dm[1][2])
        self.assertAlmostEqual(15.58845726811989564, dm[1][3])
        self.assertAlmostEqual(8.77496438739212206, dm[2][3])
        self._testSymmetry(dm)
        
    def _testSymmetry(self, dm):
        for i in range(len(dm)):
            for j in range(len(dm)):
                self.assertEqual(dm[i][j], dm[j][i])
        
class CalcDistanceMatrixFastTestCase(CalcDistanceMatrixTestCase):
    def setUp(self):
        self.distanceMatrixFunc = "calcDistanceMatrixFastEuclidean"
 
class CalcDistanceMatrixFast2TestCase(CalcDistanceMatrixTestCase):
    def setUp(self):
        self.distanceMatrixFunc = "calcDistanceMatrixFastEuclidean2"
 
