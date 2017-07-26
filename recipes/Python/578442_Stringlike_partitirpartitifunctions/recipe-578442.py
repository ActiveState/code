def partition(L, sep, key=None):
    """\
partition(list, sep, key) -> (head, sep, tail)

Search for the separator sep in list, and return the part before it,
the separator itself, and the part after it.  If the separator is not
found, return the list, None, and an empty list.

key specifies a function of one argument that is used to extract a
comparison key from each list element.

>>> for i in xrange(5):
...     print partition(range(4), i)
([], 0, [1, 2, 3])
([0], 1, [2, 3])
([0, 1], 2, [3])
([0, 1, 2], 3, [])
([0, 1, 2, 3], None, [])
"""
    if key:
        sep = key(sep)
        for i, item in enumerate(L):
            if sep == key(item):
                return L[:i], L[i], L[i+1:]
        return L, None, []
    else:
        try:
            i = L.index(sep)
            return L[:i], L[i], L[i+1:]
        except ValueError:
            return L, None, []

def rpartition(L, sep, key=None):
    """\
partition(list, sep, key) -> (head, sep, tail)

Search for the separator sep in list, starting at the end of list, and
return the part before it, the separator itself, and the part after
it.  If the separator is not found, return an empty list, None, and
the list.

key specifies a function of one argument that is used to extract a
comparison key from each list element.

>>> for i in xrange(5):
...     print rpartition(range(4), i)
([], 0, [1, 2, 3])
([0], 1, [2, 3])
([0, 1], 2, [3])
([0, 1, 2], 3, [])
([], None, [0, 1, 2, 3])
"""
    if not key:
        key = lambda x: x
    sep = key(sep)
    for i, item in enumerate(reversed(L)):
        if sep == key(item):
            i = len(L) - i - 1
            return L[:i], L[i], L[i+1:]
    return [], None, L

if __name__ == "__main__":
    import doctest
    doctest.testmod()
