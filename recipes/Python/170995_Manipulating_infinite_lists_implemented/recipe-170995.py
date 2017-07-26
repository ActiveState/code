"""Collection of useful functions which work on infinite lists.

The infinite lists are actually the generator objects. Note that
the functions will have side effects on the passed-in gLists.

"""
from __future__ import generators

def gInfinite(obj):
    """Return infinite list of repeated objects obj"""
    while 1:
        yield obj

gNone = gInfinite(None)     

def gJoin(gl1, gl2):
    """Return gl1+gl2, i.e [gl1[0],...,gl1[n],gl2[0],...]
    
    Apparently only useful when gl1 is finite.
    
    """
    for x in gl1:
        yield x
    for x in gl2:
        yield x

def gCon(x, xs):
    """Return [x, xs[0], xs[1], ...]"""
    yield x
    xs = iter(xs) # make sure it also works for ordinary list
    while 1:
        yield xs.next()

def gRange(start=0,step=1,stop=None):
    """Generalized version of range() - could be infinite
    
    Note the difference in the order of arguments from those
    of range().
    
    """
    if stop is None:
        x = int(start)
        step = int(step)
        while 1:
            yield x
            x += step
    else:
        for x in range(start, stop, step):
            yield x

def gMap(f, *gLists):
    """Generalized version of map() - work on infinite list
    
    Work differently from map(), stops when the end of the shortest
    gList is reached.
    
    """
    if f is None:
        f = lambda *x: x
    gLists = map(iter, gLists) # make sure it also works for ordinary list
    while 1:
        yield f(*[gl.next() for gl in gLists])
        
def gZip(*gLists):
    """Generalized version of zip() - work on infinite list"""
    for x in gMap(None, *gLists):
        yield x

def gFilter(f, gList):
    """Generalized version of filter() - work on infinite list"""
    if f is None:
        f = lambda x: x
    for x in gList:
        # WARNING: may fall into forever loop
        # without yielding anything if f(x) is
        # always false from a certain x onwards
        if f(x):
            yield x
            
def gCompre(f, gList, cond = lambda *x: 1):
    """List Comprehension
    
    [f(*x) for x in gList if cond(*x)]
    
    """
    for x in gList:
        # WARNING: may fall into forever loop
        # without yielding anything if f(*x) is
        # always false from a certain x onwards
        if cond(*x):
            yield f(*x)

def pList(gList, limit=20):
    """Return partial ordinary list of gList."""
    if type(gList) is type(gNone):
        return [pList(x[0]) for x in zip(gList, range(limit))]
    else:
        return gList

if __name__=='__main__':
    print pList(gMap(lambda x,y,z: x+y+z, gRange(1), gRange(2,2), gRange(3,3)))
    # -> [1+2+3, 2+4+6, 3+6+9, ...]
    
    def f(x,y):
        return '%s%i' % (x,y)
    def g(x,y):
        return y%3==0
    print pList(gCompre(f, gZip(gInfinite('A'), gRange(2)), g))
    # or pList(gCompre(lambda x,y: '%s%i' % (x,y), gZip(gInfinite('A'), gRange(2)), lambda x,y: y%3==0))
    # -> ['A3', 'A6', 'A9', ...]
    
    def sieve(gList):
        """Sieve of Eratosthene"""
        x = gList.next()
        xs = sieve(gFilter(lambda y: y % x != 0, gList))
        for y in gCon(x, xs):
            yield y

    import sys
    sys.setrecursionlimit(sys.maxint) # needed for bigger lists of primes
    primes = sieve(gRange(2)) # infinite list of primes
    print pList(primes, 100) # print the first 100 primes
    print pList(primes, 500) # print subsequent 500 primes

    # gList of gLists
    print pList(gMap(gRange, gRange()))
