'Demonstrate effective use of super()'

import collections
import logging

logging.basicConfig(level='INFO')

class LoggingDict(dict):
    # Simple example of extending a builtin class
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super(LoggingDict, self).__setitem__(key, value)

class LoggingOD(LoggingDict, collections.OrderedDict):
    # Build new functionality by reordering the MRO
    pass

ld = LoggingDict([('red', 1), ('green', 2), ('blue', 3)])
print ld
ld['red'] = 10

ld = LoggingOD([('red', 1), ('green', 2), ('blue', 3)])
print ld
ld['red'] = 10
print '-' * 20

# ------- Show the order that the methods are called ----------

def show_call_order(cls, methname):
    'Utility to show the call chain'
    classes = [cls for cls in cls.__mro__ if methname in cls.__dict__]
    print '  ==>  '.join('%s.%s' % (cls.__name__, methname) for cls in classes)

show_call_order(LoggingOD, '__setitem__')
show_call_order(LoggingOD, '__iter__')
print '-' * 20

# ------- Validate and document any call order requirements -----

position = LoggingOD.__mro__.index
assert position(LoggingDict) < position(collections.OrderedDict)
assert position(collections.OrderedDict) < position

# ------- Getting the argument signatures to match --------------

class Shape(object):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super(Shape, self).__init__(**kwds)

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super(ColoredShape, self).__init__(**kwds)

cs = ColoredShape(color='red', shapename='circle')

# -------- Making sure a root exists ----------------------------

class Root(object):
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(Root, self), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super(Shape, self).__init__(**kwds)
    def draw(self):
        print 'Drawing.  Setting shape to:', self.shapename
        super(Shape, self).draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super(ColoredShape, self).__init__(**kwds)
    def draw(self):
        print 'Drawing.  Setting color to:', self.color
        super(ColoredShape, self).draw()

ColoredShape(color='blue', shapename='square').draw()
print '-' * 20

# ------- Show how to incorporate a non-cooperative class --------

class Moveable(object):
    # non-cooperative class that doesn't use super()
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        print 'Drawing at position:', self.x, self.y

class MoveableAdapter(Root):
    # make a cooperative adapter class for Moveable
    def __init__(self, x, y, **kwds):
        self.moveable = Moveable(x, y)
        super(MoveableAdapter, self).__init__(**kwds)
    def draw(self):
        self.moveable.draw()
        super(MoveableAdapter, self).draw()

class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

MovableColoredShape(color='red', shapename='triangle', x=10, y=20).draw()

# -------- Complete example ------------------------------------

from collections import Counter, OrderedDict

class OrderedCounter(Counter, OrderedDict):
     'Counter that remembers the order elements are first encountered'

     def __repr__(self):
         return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

     def __reduce__(self):
         return self.__class__, (OrderedDict(self),)

oc = OrderedCounter('abracadabra')
print oc
