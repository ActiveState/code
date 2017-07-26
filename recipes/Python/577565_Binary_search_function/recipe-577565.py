#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze on 2011-02-04
#  This code may be used pursuant to the MIT License.
######################################################################

import __builtin__

__all__ = (
    'lower_bound',
    'upper_bound'
)

def lower_bound(haystack, needle, lo = 0, hi = None, cmp = None, key = None):
    """lower_bound(haystack, needle[, lo = 0[, hi = None[, cmp = None[, key = None]]]]) => n

Find \var{needle} via a binary search on \var{haystack}.  Returns the
index of the first match if \var{needle} is found, else a negative
value \var{N} is returned indicating the index where \var{needle}
belongs with the formula "-\var{N}-1".

\var{haystack} - the ordered, indexable sequence to search.
\var{needle} - the value to locate in \var{haystack}.
\var{lo} and \var{hi} - the range in \var{haystack} to search.
\var{cmp} - the cmp function used to order the \var{haystack} items.
\var{key} - the key function used to extract keys from the elements.
"""
    if cmp is None: cmp = __builtin__.cmp
    if key is None: key = lambda x: x
    if lo < 0: raise ValueError( 'lo cannot be negative' )
    if hi is None: hi = len(haystack)

    val = None
    while lo < hi:
        mid = (lo + hi) >> 1
        val = cmp(key(haystack[mid]), needle)
        if val < 0:
            lo = mid + 1
        else:
            hi = mid
    if val is None: return -1
    elif val == 0: return lo
    elif lo >= len(haystack): return -1 - lo
    elif cmp(key(haystack[lo]), needle) == 0: return lo
    else: return -1 - lo

def upper_bound(haystack, needle, lo = 0, hi = None, cmp = None, key = None):
    """upper_bound(haystack, needle[, lo = 0[, hi = None[, cmp = None[, key = None]]]]) => n

Find \var{needle} via a binary search on \var{haystack}.  Returns the
non-negative index \var{N} of the element that immediately follows the
last match of \var{needle} if \var{needle} is found, else a negative
value \var{N} is returned indicating the index where \var{needle}
belongs with the formula "-\var{N}-1".

\var{haystack} - the ordered, indexable sequence to search.
\var{needle} - the value to locate in \var{haystack}.
\var{lo} and \var{hi} - the range in \var{haystack} to search.
\var{cmp} - the cmp function used to order the \var{haystack} items.
\var{key} - the key function used to extract keys from the elements.
"""
    if cmp is None: cmp = __builtin__.cmp
    if key is None: key = lambda x: x
    if lo < 0: raise ValueError( 'lo cannot be negative' )
    if hi is None: hi = len(haystack)

    val = None
    while lo < hi:
        mid = (lo + hi) >> 1
        val = cmp(key(haystack[mid]), needle)
        if val > 0:
            hi = mid
        else:
            lo = mid + 1
    if val is None: return -1
    elif val == 0: return lo
    elif lo > 0 and cmp(key(haystack[lo - 1]), needle) == 0: return lo
    else: return -1 - lo

if __name__ == '__main__':
    from assertions import *

    a = [0, 2, 4, 6, 8]
    b = [0, 2, 2, 4, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8, 8]
    test_left = (
        (-1, [] , -2), (-1, [] , -1), (-1, [] , 0), (-1, [] , 1), (-1, [] , 2),
        (-1, [0], -2), (-1, [0], -1), ( 0, [0], 0), (-2, [0], 1), (-2, [0], 2),
        (-1, [1], -2), (-1, [1], -1), (-1, [1], 0), ( 0, [1], 1), (-2, [1], 2),

        (-1, [0, 0], -2), (-1, [0, 0], -1), ( 0, [0, 0], 0), (-3, [0, 0], 1), (-3, [0, 0], 2),
        (-1, [0, 1], -2), (-1, [0, 1], -1), ( 0, [0, 1], 0), ( 1, [0, 1], 1), (-3, [0, 1], 2),
        (-1, [1, 1], -2), (-1, [1, 1], -1), (-1, [1, 1], 0), ( 0, [1, 1], 1), (-3, [1, 1], 2),

        (-1, a, -1),
        ( 0, a,  0), (-2, a,  1), ( 1, a,  2), (-3, a,  3), ( 2, a,  4),
        (-4, a,  5), ( 3, a,  6), (-5, a,  7), ( 4, a,  8), (-6, a,  9),
        (-6, a, 10),

        (-1, b, -1),
        ( 0, b,  0), (-2, b,  1), (  1, b,  2), (-4, b,  3), (  3, b,  4),
        (-7, b,  5), ( 6, b,  6), (-11, b,  7), (10, b,  8), (-16, b,  9),
        (-16, b, 10)
    )
    for expect, haystack, needle in test_left:
        assertEquals(expect, lower_bound(haystack, needle), 'haystack: %r - needle: %r' % (haystack, needle))

    a = list(a)
    for i in xrange(11):
        n = lower_bound(a, i - 1)
        if n < 0:
            a[-n-1:-n-1] = [i-1]
    assertEquals([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], a)

    b = list(b)
    for i in xrange(11):
        n = lower_bound(b, i - 1)
        if n < 0:
            b.insert(-n-1, i-1)
    assertEquals([-1, 0, 1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 6, 6, 7, 8, 8, 8, 8, 8, 9], b)

    a = [0, 2, 4, 6, 8]
    b = [0, 2, 2, 4, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8, 8]
    test_right = (
        (-1, [] , -2), (-1, [] , -1), (-1, [] , 0), (-1, [] , 1), (-1, [] , 2),
        (-1, [0], -2), (-1, [0], -1), ( 1, [0], 0), (-2, [0], 1), (-2, [0], 2),
        (-1, [1], -2), (-1, [1], -1), (-1, [1], 0), ( 1, [1], 1), (-2, [1], 2),

        (-1, [0, 0], -2), (-1, [0, 0], -1), ( 2, [0, 0], 0), (-3, [0, 0], 1), (-3, [0, 0], 2),
        (-1, [0, 1], -2), (-1, [0, 1], -1), ( 1, [0, 1], 0), ( 2, [0, 1], 1), (-3, [0, 1], 2),
        (-1, [1, 1], -2), (-1, [1, 1], -1), (-1, [1, 1], 0), ( 2, [1, 1], 1), (-3, [1, 1], 2),

        (-1, a, -1),
        ( 1, a,  0), (-2, a,  1), ( 2, a,  2), (-3, a,  3), ( 3, a,  4),
        (-4, a,  5), ( 4, a,  6), (-5, a,  7), ( 5, a,  8), (-6, a,  9),
        (-6, a, 10),

        (-1, b, -1),
        ( 1, b,  0), (-2, b,  1), (  3, b,  2), (-4, b,  3), (  6, b,  4),
        (-7, b,  5), (10, b,  6), (-11, b,  7), (15, b,  8), (-16, b,  9),
        (-16, b, 10)
    )
    for expect, haystack, needle in test_right:
        assertEquals(expect, upper_bound(haystack, needle), 'haystack: %r - needle: %r' % (haystack, needle))
    for i in xrange(11):
        n = upper_bound(a, i - 1)
        if n < 0:
            a.insert(-n-1, i-1)
    assertEquals([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], a)

    import random
    a = list(xrange(100))
    b = list(a)
    for j in xrange(10):
        c = list()
        random.shuffle(b)
        for i in b:
            n = lower_bound(c, i)
            assertTrue(n < 0)
            c[-n-1:-n-1] = [i]
        assertEquals(a, c)

    def rcmp(x, y):
        return cmp(y, x)

    a.sort(cmp = rcmp)
    b.sort(cmp = rcmp)
    for j in xrange(10):
        c = list()
        random.shuffle(b)
        for i in b:
            n = lower_bound(c, i, cmp = rcmp)
            assertTrue(n < 0)
            c.insert(-n-1, i)
        assertEquals(a, c)
