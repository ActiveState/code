"""
A module for finite arithmetic.
"""


#Import generators.
from __future__ import generators


__version__ = '1.0'
__needs__ = '2.2'
__author__ = "G. Rodrigues"


#The stupidest prime-detection algorithm possible.
def IsPrime(n):
    if isinstance(n, int) and n >= 1:
        for i in range(2, n):
            if not n%i
                return 0
        return 1
    else:
        raise TypeError("%r is not an integer >= 1." % n)


#Auxiliary constructor functions.
def _ret_new(n):
    def _new(cls, m):
        if isinstance(m, int):
            return int.__new__(cls, m%n)
        else:
            raise TypeError("%r is not an integer." % m)
    return _new

def _ret_str():
    def _str(m):
        return int.__str__(m)
    return _str

def _ret_nonzero():
    def _nonzero(m):
        return int.__nonzero__(m)
    return _nonzero

def _ret_hash():
    def _hash(m):
        return int.__hash__(m)
    return _hash

def _ret_cmp():
    def _cmp(m, p):
        return int.__cmp__(m, p)
    return _cmp

def _ret_neg():
    def _neg(m):
        return m.__class__(int.__neg__(m))
    return _neg

def _ret_add():
    def _add(m, p):
        return p.__class__(int.__add__(m, p))
    return _add

def _ret_radd():
    def _radd(m, p):
        return p.__add__(m)
    return _radd

def _ret_sub():
    def _sub(m, p):
        return p.__class__(int.__sub__(m, p))
    return _sub

def _ret_rsub():
    def _rsub(m, p):
        return p.__sub__(m)
    return _rsub

def _ret_mul():
    def _mul(m, p):
        return p.__class__(int.__mul__(m, p))
    return _mul

def _ret_rmul():
    def _rmul(m, p):
        return p.__mul__(m)
    return _rmul

def _ret_div():
    def _div(m, p):
        if p:
            return p.__class__(int.__mul__(m, p.__invert__()))
        else:
            raise ZeroDivisionError("Cannot divide by zero.")
    return _div

def _ret_rdiv():
    def _rdiv(m, p):
        return p.__div__(m)
    return _rdiv

def _ret_inv(n):
    def _inv(m):
        if m:
            #Initialize variables.
            o = (m, n)
            ret = (0, 1)
            r = m % n
            q = m // n

            #Main loop.
            while 1:
                #Are we finished?
                if r:
                    o = o[-1], r
                    r = o[0] % o[1]
                    q = o[0] // o[1]
                    ret = ret[-1], ret[0] - q*ret[1]
                else:
                    return m.__class__(ret[0])
        else:
            raise ZeroDivisionError("Cannot invert 0 in any field.")
    return _inv

class Field(type):
    """The Finite Field metaclass.

    For each integer n > 1, Field(n) returns the finite ring of integers modulo n."""

    def __new__(cls, n):
        if isinstance(n, int) and n > 1:
            #Initialize methods dictionary and add the methods one by one.
            meth = {}
            
            meth['__new__'] = staticmethod(_ret_new(n))
            meth['__str__'] = _ret_str()
            meth['__nonzero__'] = _ret_nonzero()
            meth['__hash__'] = _ret_hash()
            meth['__cmp__'] = _ret_cmp()

            #Algebraic ring operations.
            meth['__neg__'] = _ret_neg()
            meth['__add__'] = _ret_add()
            meth['__radd__'] = _ret_radd()
            meth['__sub__'] = _ret_sub()
            meth['__rsub__'] = _ret_rsub()
            meth['__mul__'] = _ret_mul()
            meth['__rmul__'] = _ret_rmul()

            #If n is prime add division.
            if IsPrime(n):
                meth['__invert__'] = _ret_inv(n)
                meth['__div__'] = _ret_div()
                meth['__rdiv__'] = _ret_rdiv()

            return type.__new__(cls, "Z(%d)" % n, (int,), meth)
        else:
            raise TypeError("%s is not an integer > 1." % n)

    def __init__(self, n):
        #Generate docstring.
        self.__doc__ = "The Z(%d) finite field." % n

    def __str__(self):
        return self.__name__

    def __len__(self):
        return int(self.__name__[2:-1])

    def __iter__(self):
        for i in xrange(len(self)):
            yield self(i)


#Auxiliary functions that build the operation tables.
def cartesian_product(list1, list2):
    """Returns the cartesian product of the lists."""
    ret = []
    for i in list1:
        ret.append([(i, j) for j in list2])
    return ret

def build_table(ring, unboundmethod):
    """Displays the table for the given operation of the ring."""
    list_elems = list(ring)
    print "   " + " | ".join([str(i) for i in list_elems])

    #Main loop.    
    for lst in cartesian_product(list_elems, list_elems):
        temp = []
        for i, j in lst:
            temp.append(unboundmethod(i, j))
        print ("%s| " % lst[0][0]) + " | ".join([str(i) for i in temp])
    
def build_div(ring):
    """Displays the table for division in the ring."""
    list_elems = list(ring)
    print "   " + " | ".join([str(i) for i in list_elems])

    #Main loop.
    for lst in cartesian_product(list_elems, list_elems):
        temp = []
        for i, j in lst:
            try:
                result = i / j
            except ZeroDivisionError:
                temp.append('X')
            else:
                temp.append(result)
        print ("%s| " % lst[0][0]) + " | ".join([str(i) for i in temp])


#Some test code.
if __name__ == "__main__":
    #Construct rings.
    rings = [Field(i) for i in range(2, 10)]

    for ring in rings:
        #Test classes.
        print "This is the finite ring %s." % ring
        print "It has elements: %s." % list(ring)
        #Display tables.
        print "The addition table is:"
        build_table(ring, ring.__add__)
        print "The multiplication table is:"
        build_table(ring, ring.__mul__)
        if IsPrime(len(ring)):
            print "The division table is:"
            build_div(ring)
        else:
            print "The ring %s is not a Field." % ring
        print '\n'

    #Test silent conversions to int.
    ints = range(len(rings[-1]))
    for i, j in zip(ints, list(rings[-1])):
        print "%s + %s = %s with type %s." % (i, j, i + j, type(i + j))
