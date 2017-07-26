# Implementation 1: not portable

import sys

def fn(gen):
    """Turns a generator expression into a callable."""
    def anonymous(*args):
        return gen.next()
    return anonymous

def args():
    """Works with fn(); yields args passed to anonymous()."""
    while True:
        # Stack frame will look like:
        #   anonymous(args=(...))      "foo(3,4,5)"
        #   gen.next()                 "return gen.next()"
        #   args.next()                internal genexp code
        yield sys._getframe(2).f_locals['args']
args = args()

foo = fn(a + b * c for (a,b,c) in args)
assert foo(3,4,5) == 3+4*5
assert foo(4,5,6) == 4+5*6

# Implementation 2: not thread-safe (but it could be)

class SingleElementIterator:
    """Iterator that must be constantly fed by assigning to .value"""
    def __iter__(self):
        return self
    def next(self):
        value = self.value
        del self.value
        return value
args2 = SingleElementIterator()

def fn2(gen):
    """Turns a generator expression into a callable."""
    def anonymous(*args_):
        args2.value = args_
        return gen.next()

    return anonymous

foo = fn2(a + b * c for (a,b,c) in args2)
assert foo(3,4,5) == 3+4*5
assert foo(4,5,6) == 4+5*6
