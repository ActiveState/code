class A (object) :
    """A simple class with some internal default values"""
    def __init__ (self, x) :
        self.x     = x
        self._a    = 1000
        self._b    = 10000
        self._data = [1,2,3,4]
        self._d    = { 1 :1, 2:2, 3:3}

class A_Metaclass (type) :
    """Metaclass setting default values"""
    def __init__ (cls, name, bases, dct) :
        super(A_Metaclass, cls).__init__(name, bases, dct)
        setattr (cls, "_a",    1000)
        setattr (cls, "_b",    10000)
        setattr (cls, "_data", [1,2,3,4])
        setattr (cls, "_d",    { 1 :1, 2:2, 3:3})


class A_With_Metaclass (object) :
    """The same class as A, but internal default values set by metaclass"""
    __metaclass__ = A_Metaclass
    def __init__ (self, x) :
        self.x = x
        
from timeit import timeit
n = 10000000
print "metaclass :", timeit ("A_With_Metaclass (22)", setup = "from __main__ import A_Metaclass, A_With_Metaclass", number = n)
print "normal    :", timeit ("A                (22)", setup = "from __main__ import A",  number = n)
