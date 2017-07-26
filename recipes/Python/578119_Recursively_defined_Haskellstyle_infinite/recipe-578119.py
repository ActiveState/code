from itertools import imap, chain, count, islice, groupby, tee
from operator import add, mul
from heapq import merge

class clone(object):
    '''A decorator to simplify the creation of recursively defined generators.'''
    def __init__(self, generator):
        self.clones = iter(tee(generator()))
        self.cache = None
    def __call__(self):
        try:
            self.cache = next(self.clones)
            return next(self.clones) 
        except StopIteration:
            self.clones = iter(tee(self.cache))
            return next(self.clones)

# examples #

# helper function
def itail(iterable):
    return islice(iterable, 1, None)

# Haskell -- fibonacci
# fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

@clone
def fibs():
    for i in chain([0, 1], imap(add, fibs(), itail(fibs()))):
        yield i

# Haskell -- factorial
# facs = 1 : zipWith (*) [1 ..] facs

@clone
def facs():
    for i in chain([1], imap(mul, count(1), facs())):
        yield i

# Haskell -- http://rosettacode.org/wiki/Hamming_numbers
#
# hamming = 1 : map (2*) hamming `union` map (3*) hamming `union` map (5*) hamming 
#
# union a@(x:xs) b@(y:ys) = case compare x y of
#            LT -> x : union  xs  b
#            EQ -> x : union  xs  ys
#            GT -> y : union  a   ys


# hamming numbers generator adapted from Raymond Hettinger's algorithm
# http://code.activestate.com/recipes/576961-technique-for-cyclical-iteration/

@clone
def hamming():
        for i in (k for k, v in groupby(chain([1],
                                              merge((2*x for x in hamming()),
                                                    (3*x for x in hamming()),
                                                    (5*x for x in hamming()))))):
            yield i
