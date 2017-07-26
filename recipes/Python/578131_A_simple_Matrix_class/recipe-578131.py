import random
import operator
import sys
import unittest

__version__ = "0.3"

class MatrixError(Exception):
    """ An exception class for Matrix """
    pass

class Matrix(object):
    """ A simple Python matrix class with
    basic operations and operator overloading """
    
    def __init__(self, m, n, init=True):
        if init:
            self.rows = [[0]*n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n
        
    def __getitem__(self, idx):
        return self.rows[idx]

    def __setitem__(self, idx, item):
        self.rows[idx] = item
        
    def __str__(self):
        s='\n'.join([' '.join([str(item) for item in row]) for row in self.rows])
        return s + '\n'

    def __repr__(self):
        s=str(self.rows)
        rank = str(self.getRank())
        rep="Matrix: \"%s\", rank: \"%s\"" % (s,rank)
        return rep
    
    def reset(self):
        """ Reset the matrix data """
        self.rows = [[] for x in range(self.m)]
                     
    def transpose(self):
        """ Transpose the matrix. Changes the current matrix """
        
        self.m, self.n = self.n, self.m
        self.rows = [list(item) for item in zip(*self.rows)]

    def getTranspose(self):
        """ Return a transpose of the matrix without
        modifying the matrix itself """
        
        m, n = self.n, self.m
        mat = Matrix(m, n)
        mat.rows =  [list(item) for item in zip(*self.rows)]
        
        return mat

    def getRank(self):
        return (self.m, self.n)

    def __eq__(self, mat):
        """ Test equality """

        return (mat.rows == self.rows)
        
    def __add__(self, mat):
        """ Add a matrix to this matrix and
        return the new matrix. Doesn't modify
        the current matrix """
        
        if self.getRank() != mat.getRank():
            raise MatrixError, "Trying to add matrixes of varying rank!"

        ret = Matrix(self.m, self.n)
        
        for x in range(self.m):
            row = [sum(item) for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __sub__(self, mat):
        """ Subtract a matrix from this matrix and
        return the new matrix. Doesn't modify
        the current matrix """
        
        if self.getRank() != mat.getRank():
            raise MatrixError, "Trying to add matrixes of varying rank!"

        ret = Matrix(self.m, self.n)
        
        for x in range(self.m):
            row = [item[0]-item[1] for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __mul__(self, mat):
        """ Multiple a matrix with this matrix and
        return the new matrix. Doesn't modify
        the current matrix """
        
        matm, matn = mat.getRank()
        
        if (self.n != matm):
            raise MatrixError, "Matrices cannot be multipled!"
        
        mat_t = mat.getTranspose()
        mulmat = Matrix(self.m, matn)
        
        for x in range(self.m):
            for y in range(mat_t.m):
                mulmat[x][y] = sum([item[0]*item[1] for item in zip(self.rows[x], mat_t[y])])

        return mulmat

    def __iadd__(self, mat):
        """ Add a matrix to this matrix.
        This modifies the current matrix """

        # Calls __add__
        tempmat = self + mat
        self.rows = tempmat.rows[:]
        return self

    def __isub__(self, mat):
        """ Add a matrix to this matrix.
        This modifies the current matrix """

        # Calls __sub__
        tempmat = self - mat
        self.rows = tempmat.rows[:]     
        return self

    def __imul__(self, mat):
        """ Add a matrix to this matrix.
        This modifies the current matrix """

        # Possibly not a proper operation
        # since this changes the current matrix
        # rank as well...
        
        # Calls __mul__
        tempmat = self * mat
        self.rows = tempmat.rows[:]
        self.m, self.n = tempmat.getRank()
        return self

    def save(self, filename):
        open(filename, 'w').write(str(self))
        
    @classmethod
    def _makeMatrix(cls, rows):

        m = len(rows)
        n = len(rows[0])
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise MatrixError, "inconsistent row length"
        mat = Matrix(m,n, init=False)
        mat.rows = rows

        return mat
        
    @classmethod
    def makeRandom(cls, m, n, low=0, high=10):
        """ Make a random matrix with elements in range (low-high) """
        
        obj = Matrix(m, n, init=False)
        for x in range(m):
            obj.rows.append([random.randrange(low, high) for i in range(obj.n)])

        return obj

    @classmethod
    def makeZero(cls, m, n):
        """ Make a zero-matrix of rank (mxn) """

        rows = [[0]*n for x in range(m)]
        return cls.fromList(rows)

    @classmethod
    def makeId(cls, m):
        """ Make identity matrix of rank (mxm) """

        rows = [[0]*m for x in range(m)]
        idx = 0
        
        for row in rows:
            row[idx] = 1
            idx += 1

        return cls.fromList(rows)
    
    @classmethod
    def readStdin(cls):
        """ Read a matrix from standard input """
        
        print 'Enter matrix row by row. Type "q" to quit'
        rows = []
        while True:
            line = sys.stdin.readline().strip()
            if line=='q': break

            row = [int(x) for x in line.split()]
            rows.append(row)
            
        return cls._makeMatrix(rows)

    @classmethod
    def readGrid(cls, fname):
        """ Read a matrix from a file """

        rows = []
        for line in open(fname).readlines():
            row = [int(x) for x in line.split()]
            rows.append(row)

        return cls._makeMatrix(rows)

    @classmethod
    def fromList(cls, listoflists):
        """ Create a matrix by directly passing a list
        of lists """

        # E.g: Matrix.fromList([[1 2 3], [4,5,6], [7,8,9]])

        rows = listoflists[:]
        return cls._makeMatrix(rows)
        

class MatrixTests(unittest.TestCase):

    def testAdd(self):
        m1 = Matrix.fromList([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix.fromList([[7, 8, 9], [10, 11, 12]])        
        m3 = m1 + m2
        self.assertTrue(m3 == Matrix.fromList([[8, 10, 12], [14,16,18]]))

    def testSub(self):
        m1 = Matrix.fromList([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix.fromList([[7, 8, 9], [10, 11, 12]])        
        m3 = m2 - m1
        self.assertTrue(m3 == Matrix.fromList([[6, 6, 6], [6, 6, 6]]))

    def testMul(self):
        m1 = Matrix.fromList([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix.fromList([[7, 8], [10, 11], [12, 13]])
        self.assertTrue(m1 * m2 == Matrix.fromList([[63, 69], [150, 165]]))
        self.assertTrue(m2*m1 == Matrix.fromList([[39, 54, 69], [54, 75, 96], [64, 89, 114]]))

    def testTranspose(self):

        m1 = Matrix.makeRandom(25, 30)
        zerom = Matrix.makeZero(25, 30)
        m2 = m1 + zerom
        
        m1.transpose()
        m1.transpose()
        self.assertTrue(m2 == m1)

        # Also test getTranspose
        m2 = m1.getTranspose()
        r2 = m2.getRank()

        self.assertTrue(r2==(30,25))
        m2.transpose()

        self.assertTrue(m2 == m1)

    def testId(self):

        m1 = Matrix.makeId(10)
        m2 = Matrix.makeRandom(4, 10)
        m3 = m2*m1
        self.assertTrue(m3 == m2)

if __name__ == "__main__":
    unittest.main()
