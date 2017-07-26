__all__ = ['Iter']

from itertools import *

class Iter(object):
    '''A wrapper class providing a rich-iterator API.
    
    From the user point of view, this class supersedes the builtin iter()
    function: like iter(), it is called as Iter(iterable) or (less frequently)
    as Iter(callable,sentinel) and it returns an iterator. The returned
    iterator, in addition to the basic iterator protocol, provides a rich API, 
    exposing as methods most functions of the itertools module. Notably, two 
    frequently used itertools functions, chain and islice, are conveniently 
    exposed as addition and slicing operators, respectively.
    '''

    def __init__(self, *args): self._it = iter(*args)
    def __iter__(self): return self
    def next(self): return self._it.next()
    
    def __add__(self, other): 
        if not isinstance(other,Iter):
            raise TypeError('can only add Iter (not "%s") to Iter' % 
                            other.__class__.__name__)
        return Iter(chain(self._it, other._it))
    
    def __mul__(self, num): return Iter(chain(*tee(self._it,num)))
    __rmul__ = __mul__

    def __getitem__(self, index):
        if isinstance(index, int):
            try: return islice(self._it, index, index+1).next()
            except StopIteration:
                raise IndexError('Index %d out of range' % index)
        else:
            start,stop,step = index.start, index.stop, index.step
            if start is None: start = 0
            if step is None: step = 1
            return Iter(islice(self._it, start, stop, step))

    def enumerate(self): return Iter(enumerate(self._it))
    def map(self, func): return Iter(imap(func,self))
    def zip(self, *others): return Iter(izip(self._it, *others))
    def filter(self, predicate): return Iter(ifilter(predicate,self._it))
    def filterfalse(self, predicate): return Iter(ifilterfalse(predicate,self._it))
    def cycle(self): return Iter(cycle(self._it))
    def takewhile(self, predicate): return Iter(takewhile(predicate, self._it))
    def dropwhile(self, predicate): return Iter(dropwhile(predicate, self._it))
    def groupby(self, keyfunc=None): return Iter(groupby(self._it, keyfunc))
    def copy(self):
        self._it, new = tee(self._it)
        return Iter(new)


def irange(*args):
    '''Return an Iter-wrapped xrange object.'''
    return Iter(xrange(*args))


if __name__ == '__main__':

    # Example: A composite iterator over two files specified as follows:
    # - each fetched line is right stripped.
    # - the first 3 lines of the first file are fetched.
    # - the first line of the second file is skipped and its next 4 lines are fetched.
    # - empty lines (after the right stripping) are filtered out.
    # - the remaining lines are enumerated.

    import sys
    f1,f2 = [Iter(open(f)).map(str.rstrip) for f in sys.argv[1:3]]
    for i,line in (f1[:3] + f2[1:5]).filter(None).enumerate():
        print i,repr(line)
