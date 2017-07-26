from blist import blist
from bisect import bisect_left, bisect_right
from collections import MutableMapping, namedtuple
from heapq import merge
from itertools import chain, tee
try:
    from itertools import izip
except ImportError:
    izip = zip

Interval = namedtuple('Interval', 'start stop')

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    # from the itertools module documentation recipe
    
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class IntervalMapping(MutableMapping):
    """Mapping from intervals to values.

    Intervals can be passed as object with start and stop attributes,
    making slices apt to the case. They are considered, as the usual
    Python convention works (as in e.g. range), to include the left
    but not the right extreme.

    All methods that returns keys and values return them in order.

    >>> m = IntervalMapping()
    >>> m[1:2] = 1
    >>> m[1:2]
    1
    >>> m[1.3:1.9] # Interval lookup is successful if value is homogeneous
    1
    >>> m[2:3] = 2
    >>> Interval(1.5, 2.5) in m # Lookup fails if value is not homogeneous
    False
    >>> m[3:4] = 1
    >>> m[1], m[2], m[3]
    (1, 2, 1)
    >>> 4 in m
    False
    >>> 3.99 in m
    True
    >>> m.submapping(1.5, 2.5).items()
    [(Interval(start=1.5, stop=2), 1), (Interval(start=2, stop=2.5), 2)]
    >>> m[2:3] = 1
    >>> m.items()
    [(Interval(start=1, stop=4), 1)]
    >>> del m[2:3]
    >>> 2.5 in m
    False
    >>> m.items()
    [(Interval(start=1, stop=2), 1), (Interval(start=3, stop=4), 1)]
    >>> m[1.5:] = 42 # Assignment from 1.5 to infinity
    >>> m.items()
    [(Interval(start=1, stop=1.5), 1), (Interval(start=1.5, stop=None), 42)]
    >>> m[:] = 0 # Reset all the mapping to the value 0
    >>> m.items()
    [(Interval(start=None, stop=None), 0)]
    """

    nothing = object() # marker to indicate missing value in an interval
                       # accessible to the user for usage combined with
                       # the iteritems method.
    _debug = False # mutating methods become much slower if debug is active

    def __init__(self, other={}):
        self._bounds = blist()
        self._values = blist([self.nothing])
        # Invariant: self[key] == self._values[bisect_right(self._bounds, key)]
        self.update(other)

    @classmethod
    def from_changes(cls, startval, changes):
        """Alternative constructor from an start value and iterable of changes.

        x = cls.from_changes(startval, changes)
        is equivalent (albeit more efficient) to
        x = cls()
        x[:] = startval
        for bound, val in changes:
            x[bound:] = val
        """
        
        res = cls()
        bounds, values = res._bounds, res._values
        res._values[0] = startval
        last_v = object() # compares different from anything
        for b, v in changes:
            if v == last_v:
                continue
            bounds.append(b)
            values.append(v)
            last_v = v
        return res

    def __iter__(self):
        return (interval for interval, value in self.iteritems())

    def iteritems(self, yield_nothing=False):
        """Iterate in order over the (interval, value) pairs of the mapping.

        If yield_nothing is true, the self.nothing marker is returned for
        unset intervals.
        """
        
        bounds, values, nothing = self._bounds, self._values, self.nothing

        keys = (Interval(a, b)
                for a, b in pairwise(chain([None], bounds, [None])))
        if yield_nothing:
            return izip(keys, values)
        else:
            return ((k, v) for k, v in izip(keys, values) if v is not nothing)

    def __len__(self):
        nothing = self.nothing
        return sum(v is not nothing for v in self._values)

    def __getitem__(self, key):
        bounds, values = self._bounds, self._values
        if hasattr(key, 'start') and hasattr(key, 'stop'):
            # we are indexing with an interval. we only return the value
            # if that interval is contained within one of our intervals.
            start, stop = key.start, key.stop
            lindex = bisect_right(bounds, start) if start is not None else 0
            rindex = (bisect_left(bounds, stop)
                      if stop is not None else len(bounds))
            if lindex != rindex:
                raise KeyError(key)
            return values[lindex]
        else:
            # We are indexing with a single element.
            result = values[bisect_right(bounds, key)]
            if result is self.nothing:
                raise KeyError(key)
            return result

    def submapping(self, start, stop):
        bounds, values, nothing = self._bounds, self._values, self.nothing
        
        lindex = bisect_right(bounds, start) if start is not None else 0
        rindex = (bisect_left(bounds, stop)
                  if stop is not None else len(bounds))

        res = type(self)()
        res._bounds = blist(bounds[lindex:rindex])
        res._values = blist(values[lindex:rindex + 1])
        
        if start is not None:
            res[:start] = nothing
        if stop is not None:
            res[stop:] = nothing

        return res

    def leftmost(self):
        """Return the leftmost value."""

        return self._values[0]

    def rightmost(self):
        """Return the rightmost value."""
        
        return self._values[-1]

    def __setitem__(self, interval, value):

        bounds, values, nothing = self._bounds, self._values, self.nothing

        start, stop = interval.start, interval.stop
        if start is not None and stop is not None and not start < stop:
            errmsg = "Invalid interval {0}: start >= stop"
            raise ValueError(errmsg.format(interval))

        newbounds, newvalues = [], []
        if start is None:
            i1 = None
        else:
            i1 = bisect_left(bounds, start)
            prev_value = values[i1]
            if prev_value != value:
                newbounds.append(start)
                newvalues.append(prev_value)
        if stop is None:
            i2 = None
            newvalues.append(value)
        else:
            i2 = bisect_right(bounds, stop, i1 if i1 is not None else 0)
            next_value = values[i2]
            if next_value != value:
                newbounds.append(stop)
                newvalues.append(value)

        bounds[i1:i2] = newbounds
        values[i1:i2] = newvalues

        if self._debug:
            # Check that the assignment is ok and that invariants are
            # mantained
            
            if value is nothing:
                assert start not in self
            else:
                v = self[start]
                assert start in self, (start, bounds, values)
                assert self[start] == value
            assert len(values) == len(bounds) + 1
            assert bounds == sorted(bounds)
            assert all(a != b for a, b in pairwise(bounds))
            assert all(a != b for a, b in pairwise(values))

    def __delitem__(self, interval):
        self[interval] = self.nothing

    def __repr__(self):
        return 'IntervalMapping({0})'.format(list(self.iteritems()))

    # Methods overridden for speed

    def items(self):
        return list(self.iteritems())

    def itervalues(self):
        nothing = self.nothing
        return (v for v in self._values if v is not nothing)

    def values(self):
        return list(self.itervalues())

    def clear(self):
        self._bounds[:] = []
        self._values[:] = []

    # Functions to make pickle work properly

    def __getstate__(self):
        bounds, values, nothing = self._bounds, self._values, self.nothing
        return bounds, values, [i for i, v in enumerate(values) if v is nothing]

    def __setstate__(self, state):
        nothing = self.nothing
        bounds, values, nothing_indexes = state
        self._bounds = bounds
        self._values = values
        for i in nothing_indexes:
            values[i] = nothing

def apply(func, *mappings):
    """Return a new IntervalMapping applying func to all values of mappings.
    
    For example, apply(lambda x, y: x + y, m1, m2) returns a new
    matching with the sum of values for m1 and
    m2. IntervalMapping.nothing is passed to func when the value is
    undefined.

    >>> m1 = IntervalMapping()
    >>> m2 = IntervalMapping()
    >>> m1[:] = m2[:] = 0 # avoid problems with undefined values
    >>> m1[0:2] = 1
    >>> m2[1:3] = 2
    >>> m3 = apply(lambda a, b: a + b, m1, m2)
    >>> m3[-1], m3[0], m3[1], m3[2], m3[3]
    (0, 1, 3, 2, 0)
    """

    values = [m.leftmost() for m in mappings]

    def changes():

        def start_i_value(i_m):
            i, m = i_m
            res = ((k.start, i, v) for k, v in m.iteritems(True))
            next(res)
            return res
        change_points = merge(*map(start_i_value, enumerate(mappings)))

        lastbound = None
        for bound, i, v in change_points:
            values[i] = v
            if bound != lastbound:
                yield bound, func(*values)
                lastbound = bound
        yield bound, func(*values)

    return IntervalMapping.from_changes(func(*values), changes())

if __name__ == '__main__':
    import doctest
    doctest.testmod()
