# enum.py - an object-oriented enumerated type
#
#

"""Object-oriented enumerated type

The creation of a new enumerated type (enum) is done by the creation of a class
which inherits from class 'enum' or one of its subclasses.

Items in enum are instances of the enum class. They are declared in the class
variable '__names__' and they are automatically associated to the variables
'__name__' and '__value__' which are respectively the name of the item and its
value. Each item is constant, in the sense that it cannot be directly modified.
You use specialized the enum to do so. Moreover each item is associated to a
name which belongs to the class namespace.

'__names__' may be associated to a list, a tuple or a dict. In the case of a
list or a tuple, each element must be a string representing the name of the
item. The value of this items corresponds then to its name. In the case of
'__names__' is a dict, the name of the item corresponds to the key in the
dict and its value to the value in the dict. Each name must be a string.

Each enum class has the following methods:
 - names(): returns all the item names,
 - values(): returns the list of item values,
 - has_name(name): check the existence of an item name,
 - get(itemName): take a string representing the item name and
     return the item,

Moreover, the enum type accepts certain read-only operation like len() or iter(). And it can be used in for loop.

Examples of use:

>>> from enum import enum
>>> # simple exemple
>>> class Count(enum):
...     __names__ = ['ONE', 'TWO', 'THREE']

>>> counts = [count.__value__ for count in Count]
>>> counts.sort()
>>> print counts
['ONE', 'THREE', 'TWO']
>>> print Count.ONE.__name__
ONE
>>> print Count.ONE.__name__ == Count.ONE.__value__
True
>>> print Count.has_name('TWO')
True
>>> print Count.has_name('FOUR')
False

>>> # examples with ineritance
>>> class Op(enum):
...     __names__ = {
...         'ADD': lambda x, y: x + y,
...         'SUB': lambda x, y: x - y,
...         'MUL': lambda x, y: x * y,
...         'DIV': lambda x, y: x / y,
...     }
...     
...     def eval(self, x, y):
...         return self.__value__(x, y)
    
>>> class TrueOp(Op):
...     __names__ = {
...         'DIV': lambda x, y: float(x) / float(y),
...         'POW': lambda x, y: x ** y,
...     }
    
>>> print Op.DIV.eval(2, 3)
0
>>> print TrueOp.DIV.eval(2, 3)
0.666666666667
>>> print TrueOp.DIV.eval(2, 3) == TrueOp.DIV.__value__(2, 3)
True
>>> print TrueOp.DIV.eval(2, 3) == TrueOp.['DIV'].eval(2, 3)
True
>>> print TrueOp.DIV.__name__
DIV
"""

__all__ = ['EnumType', 'enum']

class EnumType(type):
    """Enumerated base type.
    """
    
    def __new__(mcls, name, bases, dct):
        # set a default __names__ dictionary if there is none
        decl = dct.setdefault('__names__', {})
        return type.__new__(mcls, name, bases, dct)
    
    def __init__(cls, name, bases, dct):
        def _copy(cls, obj):
            """Copy the dictionnary of obj in an new instance of cls.
            """
            tmp = object.__new__(cls, cls.__name__, cls.__bases__, cls.__dict__)
            tmp.__dict__.update(obj.__dict__)
            return tmp

        type.__init__(name, bases, dct)
        # the __readonly attribute indicates Python if the enum class can be
        # modified (it is modifiable just during the initialisation)
        type.__setattr__(cls, '__readonly', False)
        decl = type.__getattribute__(cls, '__names__')
        tmp_decl = {}
        
        # get the attribute __names__ of the bases classes for inheritance
        for base in bases:
            if isinstance(base, EnumType):
                base_decl = object.__getattribute__(base, '__names__')
                for name, value in base_decl.iteritems():
                    tmp_decl[name] = _copy(cls, value)
        
        # convert each __names__ item to an instance of the current class
        if type(decl) is dict:
            for name, value in decl.iteritems():
                tmp_decl[name] = cls(value)
                object.__setattr__(tmp_decl[name], '__name__', name)
        elif type(decl) in [list, tuple]:
            for name in decl:
                tmp_decl[name] = cls(name)
                object.__setattr__(tmp_decl[name], '__name__', name)
        else:
            raise AttributeError, 'bad __names__ declaration in %s' % cls
        
        type.__setattr__(cls, '__names__', tmp_decl)
        type.__setattr__(cls, '__readonly', True)
    
    def __getattribute__(cls, name):
        if not object.__getattribute__(cls, '__names__').has_key(name):
            if not object.__getattribute__(cls, name):
                raise AttributeError, "Unknow attribute: '%s'" % name
            return object.__getattribute__(cls, name)
        return object.__getattribute__(cls, '__names__')[name]
    
    def __setattr__(cls, name, value):
        decl = object.__getattribute__(cls, '__names__')
        if decl.has_key(name):
            raise AttributeError, "Read only instance: %s" % decl[name]
        else:
            raise AttributeError, "Read only class: %s" % cls
    
    def has_name(cls, name):
        return object.__getattribute__(cls, '__names__').has_key(name)
    
    def names(cls):
        return object.__getattribute__(cls, '__names__').values()
    
    def get(cls, name):
        return object.__getattribute__(cls, '__names__')[name]
    
    def __len__(cls):
        return len(object.__getattribute__(cls, '__names__'))
    
    def __getitem__(cls, name):
        return object.__getattribute__(cls, '__names__')[name]
    
    def __iter__(cls):
        return object.__getattribute__(cls, '__names__').itervalues()
    
    def __contains__(cls, name):
        return object.__getattribute__(cls, '__names__').has_key(name)
    
    def __repr__(cls):
        return "<EnumType '%s.%s'>" % (cls.__module__, cls.__name__)

class enum(object):
    """Enumeration base class.
    """
    __metaclass__ = EnumType
    
    def __init__(self, value):
        object.__init__(self)
        self.__value__ = value
    
    def __repr__(self):
        return "<%s.%s enum %s at %s>" % (self.__class__.__module__,
                                          self.__class__.__name__, 
                                          self.__name__,
                                          hex(id(self)))
    
    def __setattr__(self, name, value):
        if type.__getattribute__(self.__class__, '__readonly'):
            raise AttributeError, "Read only instance: %s" % self
        else:
            object.__setattr__(self, name, value)


# ---- some more tests ---------------------------

def _test():
    
    class Op(enum):
        """Some operators including integer division.
        """
        __names__ = {
            'ADD': lambda x, y: x + y, 
            'SUB': lambda x, y: x - y, 
            'MUL': lambda x, y: x * y, 
            'DIV': lambda x, y: x / y, 
        }
        def eval(self, x, y):
            return self.__value__(x, y)
        
        def __str__(self):
            return self.__name__
    
    class TrueOp(Op):
        """Some operators including true division and power.
        """
        __names__ = {
            'DIV': lambda x, y: float(x) / float(y), 
            'POW': lambda x, y: x ** y, 
        }
    
    # print the result of each operation in Op with the value 2 and 3
    # DIV must return 0
    for op in Op:
        print '%s %s %s = %s' % (2, op, 3, op.eval(2, 3))
    print ''
    
    # print the result of each operation in TrueOp with the value 2 and 3
    # DIV must return a float
    for op in TrueOp:
        print '%s %s %s = %s' % (2, op, 3, op.eval(2, 3))
    print ''
    
    print "len(Op) = %s" % len(Op)                 # must print 4
    print "len(TrueOp) = %s" % len(TrueOp)         # must print 5
    print "POW in Op = %s" % ('POW' in Op)         # must print False
    print "POW in TrueOp = %s" % ('POW' in TrueOp) # must print True
    
    print ''
    import math
    
    class SomePoint(enum):
        """An example with an inner class."""
        class Point(object):
            def __init__(self, x, y):
                self.x = x
                self.y = y
            
            def norm(self):
                return math.sqrt(self.x**2 + self.y**2)
        
        __names__ = {
             'A': Point(0, 0),
             'B': Point(1, 2),
             'C': Point(3, 2)
        }
        
        def getX(self):
            return self.__value__.x
        
        def getY(self):
            return self.__value__.y
        
        def norm(self):
            return self.__value__.norm()
    
    for point in SomePoint:
        print "(%s,%s), norm = %s" % (point.getX(), point.getY(), point.norm())

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    _test()

# End
