#!/usr/bin/env python

"""Replace a grid with one that is more coarse"""

import Numeric

def grid_coarse(in_grid, in_ny, in_nx, out_ny, out_nx, factor):
    """Replace a grid with one that is more coarse

        Inputs:
            in_ny -- number of input grid rows
            in_nx -- number of input grid columns
            out_ny -- number of output grid rows
            out_nx -- number of output grid columns
            factor -- input grid box length divided by output grid box length
            
    """

    out_grid = Numeric.zeros((out_ny, out_nx), in_grid.typecode())

    for j in xrange(0, out_ny):
        xjfine = float(j) * factor 
        jfine = int (float(j) * factor)
        dj = xjfine - float(jfine)
        jp1 = min(in_ny-1, jfine+1)
        jm1 = max(0, jfine-1)

        for i in xrange(0, out_nx):
            xifine = float(i) * factor
            ifine = int (float(i) * factor)
            di = xifine - float(ifine)
            ip1 = min(in_nx-1, ifine+1)

            xval = (1.-di) * (1.-dj) * in_grid[jfine, ifine] + (1.-di) * dj * in_grid[jp1, ifine] + di * (1.-dj) * in_grid[jfine, ip1] + di * dj * in_grid[jp1, ip1]
 
            out_grid[j, i] = xval
    return out_grid
    
class GridCoarse(object):
    """Replace a grid with one that is more coarse"""

    def __init__(self, in_ny, in_nx, out_ny, out_nx, factor):
        """Constructor
        
        Inputs:
            in_ny -- number of input grid rows
            in_nx -- number of input grid columns
            out_ny -- number of output grid rows
            out_nx -- number of output grid columns
            factor -- input grid box length divided by output grid box length
        """
        self.in_ny = in_ny
        self.in_nx = in_nx
        self.out_ny = out_ny
        self.out_nx = out_nx
        self.factor = factor

        self.jfine = Numeric.zeros(out_ny)
        self.dj = Numeric.zeros(out_ny, Numeric.Float64)
        self.jp1 = Numeric.zeros(out_ny)
        self.ifine = Numeric.zeros(out_nx)
        self.di = Numeric.zeros(out_nx, Numeric.Float64)
        self.ip1 = Numeric.zeros(out_nx)

        for j in xrange(0, out_ny):
            xjfine = float(j) * self.factor 

            self.jfine[j] = int(float(j) * self.factor)
            self.dj[j] = xjfine - float(self.jfine[j])
            self.jp1[j] = min(self.in_ny-1, self.jfine[j]+1)

        for i in xrange(0, out_nx):
            xifine = float(i) * self.factor

            self.ifine[i] = int(float(i) * self.factor)
            self.di[i] = xifine - float(self.ifine[i])
            self.ip1[i] = min (self.in_nx-1, self.ifine[i]+1)

        self.d1 = Numeric.outerproduct(1.0 - self.dj, 1.0 - self.di)
        self.d2 = Numeric.outerproduct(self.dj, 1.0 - self.di)
        self.d3 = Numeric.outerproduct(1.0 - self.dj, self.di)
        self.d4 = Numeric.outerproduct(self.dj, self.di)

    def convert(self, in_grid):
        g1 = Numeric.take(Numeric.take(in_grid, self.jfine), self.ifine, 1)
        g2 = Numeric.take(Numeric.take(in_grid, self.jp1), self.ifine, 1)
        g3 = Numeric.take(Numeric.take(in_grid, self.jfine), self.ip1, 1)
        g4 = Numeric.take(Numeric.take(in_grid, self.jp1), self.ip1, 1)
        out_grid = self.d1 * g1 + self.d2 * g2 + self.d3 * g3 + self.d4 * g4
        return out_grid.astype(in_grid.typecode())


def test1():

    in_ny = 500
    in_nx = 500
    out_ny = 250
    out_nx = 250
    factor = 2.0
    a = Numeric.arange(500*500)
    in_grid = a.resize((500, 500))
    gc = grid_coarse(in_grid, in_ny, in_nx, out_ny, out_nx, factor)

def test2():
    in_ny = 500
    in_nx = 500
    out_ny = 250
    out_nx = 250
    factor = 2.0
    a = Numeric.arange(500*500)
    in_grid = a.resize((500, 500))
    gc = GridCoarse(in_ny, in_nx, out_ny, out_nx, factor)
    out_grid = gc.convert(in_grid)





if __name__ == "__main__":

    import timeit
            

    t = timeit.Timer("test1()", "from __main__ import test1")
    print "test1(): ",
    print t.timeit(number=10)
    t = timeit.Timer("test2()", "from __main__ import test2")
    print "test2(): ",
    print t.timeit(number=10)
    

    



    
