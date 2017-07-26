"""
>>> list(zip_exc([]))
[]

>>> list(zip_exc((), (), ()))
[]

>>> list(zip_exc("abc", range(3)))
[('a', 0), ('b', 1), ('c', 2)]

>>> try:
...     list(zip_exc("", range(3)))
... except LengthMismatch:
...     print "mismatch"
mismatch

>>> try:
...     list(zip_exc(range(3), ()))
... except LengthMismatch:
...     print "mismatch"
mismatch

>>> try:
...     list(zip_exc(range(3), range(2), range(4)))
... except LengthMismatch:
...     print "mismatch"
mismatch

>>> items = zip_exc(range(3), range(2), range(4))
>>> items.next()
(0, 0, 0)
>>> items.next()
(1, 1, 1)
>>> try: items.next()
... except LengthMismatch: print "mismatch"
mismatch
"""

from itertools import chain, izip

class LengthMismatch(Exception):
    pass

def _throw():
    raise LengthMismatch
    yield None # unreachable

def _check(rest):
    for i in rest:
        try:
            i.next()
        except LengthMismatch:
            pass
        else:
            raise LengthMismatch
    return
    yield None # unreachable

def zip_exc(*iterables):
    """Like itertools.izip(), but throws a LengthMismatch exception if
    the iterables' lengths differ.
    """
    rest = [chain(i, _throw()) for i in iterables[1:]]
    first = chain(iterables[0], _check(rest))
    return izip(*[first] + rest)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
