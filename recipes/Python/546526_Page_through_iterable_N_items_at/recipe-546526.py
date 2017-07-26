class groupcount(object):
    """Accept a (possibly infinite) iterable and yield a succession
    of sub-iterators from it, each of which will yield N values.

    >>> gc = groupcount('abcdefghij', 3)
    >>> for subgroup in gc:
    ...     for item in subgroup:
    ...             print item,
    ...     print
    ...
    a b c
    d e f
    g h i
    j
    """

    def __init__(self, iterable, n=10):
        self.it = iter(iterable)
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        return self._group(self.it.next())

    def _group(self, ondeck):
        yield ondeck
        for i in xrange(1, self.n):
            yield self.it.next()
