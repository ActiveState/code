# mergeinf.py
# (C) 2010 Gabriel Genellina

from heapq import heappop, heapreplace, heapify
from operator import attrgetter

__all__ = ['imerge']

# 3.x compatibility
try:
    iter(()).next
except AttributeError:
    next_function_getter = attrgetter('__next__')
    class IterRecord(list):
      def __eq__(self, other): return self[0]==other[0]
      def __lt__(self, other): return self[0]<other[0]
      def __le__(self, other): return self[0]<=other[0]
      def __ne__(self, other): return self[0]!=other[0]
      def __gt__(self, other): return self[0]>other[0]
      def __ge__(self, other): return self[0]>=other[0]
else:    
    next_function_getter = attrgetter('next')
    IterRecord = list

    
def imerge(iterables, key=None):
    '''Merge a (possibly infinite) number of already sorted inputs 
    (each of possibly infinite length) into a single sorted output.

    Similar to heapq.merge and sorted(itertools.chain(*iterables)).

    Like heapq.merge, returns a generator, does not pull the data 
    into memory all at once, and assumes that each of the input 
    iterables is already sorted (smallest to largest).

    Unlike heapq.merge, accepts an infinite number of input iterables, 
    but requires all of them to come in ascending order (that is, 
    their starting point must come in ascending order).

    In addition, accepts a *key* function (like `sorted`, `min`, 
    `max`, etc.)
    
    >>> list(imerge([[1,3,5,7], [2,4,8], [5,10,15,20], [], [25]]))
    [1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]
    '''

    _heappop, _heapreplace, _heapify, _StopIteration = heappop, heapreplace, heapify, StopIteration
    _iter, _next, _len, _next_function_getter = iter, next, len, next_function_getter

    h = []
    h_append = h.append
    iterables = _iter(iterables)

    more_iterables = True
    while _len(h)<2:
        try:
            # raises StopIteration when no more iterables
            next_item = _next_function_getter(_iter(_next(iterables)))
        except _StopIteration:
            more_iterables = False
            break
        try:
            v = next_item()
        except _StopIteration:
            # ignore empty iterables
            continue
        if key is not None:
            highest = key(v)
        else:
            highest = v
        h_append(IterRecord([highest, v, next_item]))

    if _len(h) >= 2:
        # the heap invariant should hold, if input iterables come already sorted
        if h[1][0] < h[0][0]:
            raise ValueError('items out of order: %r and %r' % (h[0][0], h[1][0]))

    elif _len(h) == 1:
        # a single iterable, just send it
        assert not more_iterables
        _, v, next_item = h[0]
        yield v
        try:
            while True:
                yield next_item()
        except _StopIteration:
            return

    else:
        # empty
        return

    cur = highest
    while h:
        _, v, next_item = s = h[0]
        yield v

        try:
            v = s[1] = next_item()   # raises StopIteration when no more items
        except _StopIteration:
            _heappop(h)              # remove empty iterator
        else:
            if key is not None:
                cur = s[0] = key(v)
            else:
                cur = s[0] = v
            _heapreplace(h, s)       # restore heap condition

        # 'highest' is the highest known item in the heap.
        # Any time we advance an iterable and get an item ('cur')
        # greater than 'highest', we must bring more enough iterables
        # into play to ensure no items are missed.
        if more_iterables and (cur >= highest or _len(h) < 2):
            while cur >= highest or _len(h)<2:
                try:
                    # raises StopIteration when no more iterables
                    next_item = _next_function_getter(_iter(_next(iterables)))
                except _StopIteration:
                    more_iterables = False
                    break
                try:
                    v = next_item()
                except _StopIteration:
                    # ignore empty iterables
                    continue
                if key is not None:
                    highest = key(v)
                else:
                    highest = v
                h_append(IterRecord([highest, v, next_item]))
            _heapify(h)
