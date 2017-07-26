class ndim:             # from nD array to flat array
    def __init__(self,arr_dim):
        self.dimensions=arr_dim
        print "***dimensions***"
        print self.dimensions
        self.numdimensions=len(arr_dim) 
        print "***numdimension***"
        print self.numdimensions
        self.gridsize=reduce(lambda x, y: x*y, arr_dim)
        print self.gridsize
    def getcellindex(self, location):
        cindex = 0
        cdrop = self.gridsize
        for index in xrange(self.numdimensions):
            cdrop /= self.dimensions[index]
            cindex += cdrop * location[index]
        return cindex
    def getlocation(self, cellindex):
        res = []
        for size in reversed(self.dimensions):
            res.append(cellindex % size)
            cellindex /= size
        return res[::-1]

# how to use ndim class
arr_dim = [3,3,2,2]
n=ndim(arr_dim)
print "*****n.getcellindex((0,0,0,0))"
print n.getcellindex((0,0,0,0))
print "*****n.getcellindex((0,0,1,1))"
print n.getcellindex((0,0,1,1))
print "*****n.getcellindex((0,1,0,0))"
print n.getcellindex((0,1,0,0))
print "*****n.getcellindex((2,2,1,1))"
print n.getcellindex((2,2,1,1))
print
print "*****n.getlocation(0) "
print n.getlocation(0)
print "*****n.getlocation(3) "
print n.getlocation(3)
print "*****n.getlocation(4) "
print n.getlocation(4)
print "*****n.getlocation(35) "
print n.getlocation(35)
