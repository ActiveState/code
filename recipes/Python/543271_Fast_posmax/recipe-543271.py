def _posmax_psy(seq, key=None):
    """posmax(seq, key=None): return the position of the first maximum
    item of a sequence. Accepts the usual key parameter too.

    >>> posmax([])
    Traceback (most recent call last):
      ...
    ValueError: maxpos() arg is an empty sequence
    >>> posmax([1])
    0
    >>> posmax(xrange(100))
    99
    >>> posmax(xrange(100, 0, -1))
    0
    >>> posmax([1,5,0,4,3])
    1
    >>> posmax([1,5,0,4,5,3])
    1
    >>> l = ['medium', 'longest', 'short']
    >>> posmax(l)
    2
    >>> posmax(l, key=len)
    1
    >>> posmax(xrange(10**4))
    9999
    >>> posmax([2,4,-2,[4],21]) # silly comparison
    3
    >>> posmax([2,4,-2+3J,[4],21])
    Traceback (most recent call last):
      ...
    TypeError: no ordering relation is defined for complex numbers
    """
    first = True
    max_pos = 0
    pos = 0

    if key is None:
        for el in seq:
            if first:
                max_el = el
                first = False
            elif el > max_el:
                max_el = el
                max_pos = pos
            pos += 1
    else:
        for el in seq:
            key_el = key(el)
            if first:
                max_key_el = key_el
                first = False
            elif key_el > max_key_el:
                max_key_el = key_el
                max_pos = pos
            pos += 1

    if first:
        raise ValueError("maxpos() arg is an empty sequence")
    else:
        return max_pos


def _posmax_nopsy(seq, key=None):
    """posmax(seq, key=None): return the position of the first maximum
    item of a sequence. Accepts the usual key parameter too.

    >>> posmax([])
    Traceback (most recent call last):
      ...
    ValueError: maxpos() arg is an empty sequence
    >>> posmax([1])
    0
    >>> posmax(xrange(100))
    99
    >>> posmax(xrange(100, 0, -1))
    0
    >>> posmax([1,5,0,4,3])
    1
    >>> posmax([1,5,0,4,5,3])
    1
    >>> l = ['medium', 'longest', 'short']
    >>> posmax(l)
    2
    >>> posmax(l, key=len)
    1
    >>> posmax(xrange(10**4))
    9999
    >>> posmax([2,4,-2,[4],21]) # silly comparison
    3
    >>> posmax([2,4,-2+3J,[4],21])
    Traceback (most recent call last):
      ...
    TypeError: no ordering relation is defined for complex numbers
    """
    first = True
    max_pos = 0

    if key is None:
        for pos, el in enumerate(seq):
            if first:
                max_el = el
                first = False
            elif el > max_el:
                max_el = el
                max_pos = pos
    else:
        for pos, el in enumerate(seq):
            key_el = key(el)
            if first:
                max_key_el = key_el
                first = False
            elif key_el > max_key_el:
                max_key_el = key_el
                max_pos = pos

    if first:
        raise ValueError("maxpos() arg is an empty sequence")
    else:
        return max_pos


def _posmax_benchmark1():
    from time import clock
    alist = [3]*1000 + [5] + [3]*1000

    t = clock()
    for _ in xrange(60000):
        r = posmax(alist)
    print round(clock() - t, 2), r


try:
    import psyco
    psyco.full()
    posmax = _posmax_psy
except ImportError:
    posmax = _posmax_nopsy


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "Doctests finished.\n"

    _posmax_benchmark1()
