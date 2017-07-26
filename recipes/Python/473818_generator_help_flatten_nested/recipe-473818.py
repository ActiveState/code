import types
from itertools import izip, count

class Looper:
    "superclass for other loopers"
    def __init__(self):
        self.loop_counter = 0

    def next(self):
        self.loop_counter += 1
        if hasattr(self, 'get_next_value'):
            return self.get_next_value()
        else:
            raise Exception('%s has no get_next_value() method' % self)

    def reset(self, arg=None):
        self.loop_counter = 0
        if hasattr(self, 'do_reset'):
            self.do_reset(arg)
            return self.next()

class RangeLooper(Looper):
    "Loop between numeric ranges"
    def __init__(self, a, b=None, c=None):
        Looper.__init__(self)
        if (b==None) and (c==None): # only a passed in
            self.min, self.max, self.step = 0,a,1
        elif c==None: # min/max passed in
            self.min, self.max, self.step = a,b,1
        else:
            self.min, self.max, self.step = a,b,c
        self.value = self.min

    def get_next_value(self):
        result = self.value
        self.value = self.value + self.step
        return result    
    
    def is_finished(self):
        return self.value >= self.max

    def do_reset(self, arg):
        self.value = self.min

class ListLooper(Looper):
    "Loop through items in a list-like object"
    def __init__(self, list):
        Looper.__init__(self)
        self.list = list
        self.position = 0

    def get_next_value(self):
        result = self.list[self.position]
        self.position += 1
        return result

    def is_finished(self):
        return self.position >= len(self.list)

    def do_reset(self, arg):
        self.position = 0
 
class BooleanLooper(Looper):
    "Loop between True/False"
    def __init__(self, value=True):
        Looper.__init__(self)
        self.value = self.orig_value = value

    def get_next_value(self):
        self.value = not self.value
        return not self.value

    def do_reset(self, arg):
        self.value = self.orig_value

    def is_finished(self):
        return self.loop_counter > 1

class CalcField(Looper):
    "Provide a means for a calculated field, based on counters to the left of this one"
    def __init__(self, F, arg):
        Looper.__init__(self)
        
        self.F = F
        self.value = F(arg)

    def get_next_value(self):
        return self.value
    
    def is_finished(self):
        return True

    def do_reset(self, arg):
        self.value = self.F(arg)

def new_looper(a, arg=None):
    """Helper function for nest()
    determines what sort of looper to make given a's type"""
    if isinstance(a,types.TupleType):
        if len(a) == 2:
            return RangeLooper(a[0],a[1])
        elif len(a) == 3:
            return RangeLooper(a[0],a[1],a[2])
    elif isinstance(a, types.BooleanType):
        return BooleanLooper(a)
    elif isinstance(a,types.IntType) or isinstance(a, types.LongType):
        return RangeLooper(a)
    elif isinstance(a, types.StringType) or isinstance(a, types.ListType):
        return ListLooper(a)
    elif isinstance(a, Looper):
        return a
    elif isinstance(a, types.LambdaType):
        return CalcField(a, arg)

def nest(*args):
    """provide nested loop functionality in a generator context
    
    Put simply, it allows you to flatten your nested loops quite considerably..
    instead of:

    for x in range(width):
        for y in range(depth):
            for z in range(height):
                do_something(x,y,z)
    
    you can write:

    for x,y,z in nest(width, depth, height):
        do_something(x,y,z)
    
    Takes a variable number of arguments which can be:
     integer, tuple, list, string, lambda function, or Looper object

    for integer arguments, you get similar functionality to range():
    >>> for x,y in nest(3,3):
    ...     print x,y
    0 0
    0 1
    0 2
    1 0
    1 1
    1 2
    2 0
    2 1
    2 2

    Tuples let you specify the numeric range more precisely
    (2-tuple: min, max / 3-tuple: min, max, step):
    >>> for x,y in nest( (1,4), (10, 40, 10) ):
    ...     print x,y
    1 10
    1 20
    1 30
    2 10
    2 20
    2 30
    3 10
    3 20
    3 30
    
    Lists and strings are handled by pulling consecutive items (or characters) from them
    >>> for i in nest('abc', [2.5, 7, 3]):
    ...     print i
    ('a', 2.5)
    ('a', 7)
    ('a', 3)
    ('b', 2.5)
    ('b', 7)
    ('b', 3)
    ('c', 2.5)
    ('c', 7)
    ('c', 3)
    
    Boolean arguments make a loop variable which flips from True to False, initialised to the value you gave..
    >>> for i in nest(False, False, False):
    ...     print i, i[0] ^ i[1] ^ i[2]
    (False, False, False) False
    (False, False, True) True
    (False, True, False) True
    (False, True, True) False
    (True, False, False) True
    (True, False, True) False
    (True, True, False) False
    (True, True, True) True
    
    Lambda functions provide calculated fields which are only evaluated when it is their turn to increment.
    >>> for x,calc,y in nest((3,5), lambda(x): float(x[0])/10, 3):
    ...     print x, calc, y
    3 0.3 0
    3 0.3 1
    3 0.3 2
    4 0.4 0
    4 0.4 1
    4 0.4 2
    """
    n_levels = len(args)
    loopers = [None] * n_levels
    counters = []
    for i,a in izip(count(), args):
        loopers[i] = new_looper(a, counters)
        counters.append(loopers[i].next())
            
    def inc_counters(n=n_levels-1):
        "Increment counters, rightmost first"
        if n < 0:
            raise StopIteration
        if loopers[n].is_finished():
            inc_counters(n-1)
            counters[n] = loopers[n].reset(arg=counters[:n])
        else:
            counters[n] = loopers[n].next()
                
    while 1:
        yield tuple(counters)
        inc_counters()

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
