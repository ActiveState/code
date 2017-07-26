from types import NoneType # for tensor
from copy import deepcopy # for tensor


def tensor(sizes=0, elem=0):
    """tensor(sizes=0, elem=0): creates a list of lists of lists...
    The parameter sizes can be a number or a tuple/list or sizes.

    >>> tensor()
    []
    >>> tensor(())
    []

    It works with a single number or a sequence of numbers:
    >>> tensor(3)
    [0, 0, 0]
    >>> tensor((3))
    [0, 0, 0]
    >>> tensor((3), None)
    [None, None, None]
    >>> tensor((2, 3)) # array of 2 rows and 3 colums.
    [[0, 0, 0], [0, 0, 0]]
    >>> tensor((2, 3), 2)
    [[2, 2, 2], [2, 2, 2]]
    >>> tensor((1, 2, 3))
    [[[0, 0, 0], [0, 0, 0]]]
    >>> tensor((2, 2, 3))
    [[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]]

    It works with mutables too, calling deepcopy:
    >>> r = tensor((2, 3), [3])
    >>> r
    [[[3], [3], [3]], [[3], [3], [3]]]
    >>> r[0][2][0] = 0
    >>> r
    [[[3], [3], [0]], [[3], [3], [3]]]
    """
    if isinstance(sizes, (int, long)):
        sizes = [sizes]
    elif not isinstance(sizes, list):
        sizes = list(sizes)

    result = []
    if sizes:
        first = sizes.pop()
        if isinstance(elem, (int, long, basestring, tuple, NoneType, bool)):
            result = [elem] * first
        else:
            result = [deepcopy(elem) for i in xrange(first)]
        while sizes:
            result = [deepcopy(result) for i in xrange(sizes.pop())]
    return result


def transpose(m):
    """transpose(m): transposes a 2D matrix, made of tuples or lists of tuples or lists,
    keeping their type.

    >>> transpose([])
    Traceback (most recent call last):
      ...
    IndexError: list index out of range
    >>> transpose([[]])
    []
    >>> transpose([1,2,3])
    Traceback (most recent call last):
      ...
    TypeError: zip argument #1 must support iteration
    >>> transpose([[1,2,3]])
    [[1], [2], [3]]
    >>> transpose( [[2, 2, 2], [2, 2, 2]] )
    [[2, 2], [2, 2], [2, 2]]
    >>> transpose( [(2, 2, 2), (2, 2, 2)] )
    [(2, 2), (2, 2), (2, 2)]
    >>> transpose( ([2, 2, 2], [2, 2, 2]) )
    ([2, 2], [2, 2], [2, 2])
    >>> transpose( ((2, 2, 2), (2, 2, 2)) )
    ((2, 2), (2, 2), (2, 2))
    >>> t = [[[1], [2]], [[3], [4]], [[5], [6]]]
    >>> transpose(t)
    [[[1], [3], [5]], [[2], [4], [6]]]
    """
    if isinstance(m, list):
        if isinstance(m[0], list):
            return map(list, zip(*m))
        else:
            return zip(*m) # faster
    else:
        if isinstance(m[0], list):
            return tuple(map(list, zip(*m)))
        else:
            return tuple( zip(*m) )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "Tests done."
