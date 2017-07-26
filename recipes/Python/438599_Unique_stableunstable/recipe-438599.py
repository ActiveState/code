from itertools import groupby # for unique function.
from bisect import bisect_left, insort_left # for unique function.


def unique(seq, stable=False):
    """unique(seq, stable=False): return a list of the elements in seq in arbitrary
    order, but without duplicates.
    If stable=True it keeps the original element order (using slower algorithms)."""
    # Developed from Tim Peters version:
    #   http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560

    #if uniqueDebug and len(str(seq))<50: print "Input:", seq # For debugging.

    # Special case of an empty s:
    if not seq: return []

    # if it's a set:
    if isinstance(seq, set): return list(seq)

    if stable:
        # Try with a set:
        seqSet= set()
        result = []
        try:
            for e in seq:
                if e not in seqSet:
                    result.append(e)
                    seqSet.add(e)
        except TypeError:
            pass # move on to the next method
        else:
            #if uniqueDebug: print "Stable, set."
            return result

        # Since you can't hash all elements, use a bisection on sorted elements
        result = []
        sortedElem = []
        try:
            for elem in seq:
                pos = bisect_left(sortedElem, elem)
                if pos >= len(sortedElem) or sortedElem[pos] != elem:
                    insort_left(sortedElem, elem)
                    result.append(elem)
        except TypeError:
            pass  # Move on to the next method
        else:
            #if uniqueDebug: print "Stable, bisect."
            return result
    else: # Not stable
        # Try using a set first, because it's the fastest and it usually works
        try:
            u = set(seq)
        except TypeError:
            pass # move on to the next method
        else:
            #if uniqueDebug: print "Unstable, set."
            return list(u)

        # Elements can't be hashed, so bring equal items together with a sort and
        # remove them out in a single pass.
        try:
            t = sorted(seq)
        except TypeError:
            pass  # Move on to the next method
        else:
            #if uniqueDebug: print "Unstable, sorted."
            return [elem for elem,group in groupby(t)]

    # Brute force:
    result = []
    for elem in seq:
        if elem not in result:
            result.append(elem)
    #if uniqueDebug: print "Brute force (" + ("Unstable","Stable")[stable] + ")."
    return result


# Following a suggestion from Alex Martelli, sometimes this uniquePick
# is faster for more than about 300 unsortable and unhashable elements:

from cPickle import dumps

def uniquePick(seq):
    result = []
    seen = set()
    for elem in seq:
        key = dumps(elem, protocol=-1)
        if key not in seen:
             seen.add(key)
             result.append(elem)
    return result


if __name__ == '__main__': # Test
    from time import clock
    #uniqueDebug = False
    print "unique asserts" # ************************
    print "  Unstable unique..."
    assert unique( [] ) == []
    assert sorted(unique( [3, 2, 3, 1, 2] )) == [1, 2, 3]
    r = range(10**5)
    assert sorted(unique( set(r) )) == r
    s = "iterable dict based unique"
    assert sorted(unique(s)) == [' ','a','b','c','d','e','i','l','n','q','r','s','t','u']
    assert unique( [[1], [2]] ) == [[1], [2]]
    assert unique( ((1,),(2,)) ) == [(2,), (1,)]
    assert unique( ([1,],[2,]) ) == [[1], [2]]
    assert unique( ([1+2J],[2+1J],[1+2J]) ) == [[1+2j], [2+1j]]
    assert unique( ([1+2J],[1+2J]) ) == [[1+2j]]
    assert unique( [0] * 1000 ) == [0]

    print "  Stable unique..."
    assert unique( [1, 2, 3, 1, 2], True ) == [1, 2, 3]
    assert unique( [3, 2, 3, 1, 2], True ) == [3, 2, 1]
    r = range(10**5)
    assert sorted(unique( set(r), True )) == r
    s = "iterable dict based unique"
    assert unique(s, True) == ['i','t','e','r','a','b','l',' ','d','c','s','u','n','q']
    assert unique( [[1], [2]], True ) == [[1], [2]]
    assert unique( ((1,),(2,)), True ) == [(1,), (2,)]
    assert unique( ([1,],[2,]), True ) == [[1], [2]]
    assert unique( ([1+2J],[2+1J],[1+2J]), True ) == [[1+2j], [2+1j]]
    assert unique( ([1+2J],[1+2J]), True ) == [[1+2j]]
    assert unique( [0] * 1000, True ) == [0]
    assert unique( list("cbcab"), True ) == ['c', 'b', 'a']
    s = "bisect based unique"
    assert unique(s, True) == ['b', 'i', 's', 'e', 'c', 't', ' ', 'a', 'd', 'u', 'n', 'q']

    print "  unique timings:"
    #uniqueDebug = True
    print "   with a set:"
    l = range(10**5) * 10
    t = clock()
    unique( l )
    print "   ", round(clock()-t, 2)
    t = clock()
    unique( l, True )
    print "   ", round(clock()-t, 2)

    print "   with a sort/bisect:"
    l = [[e] for e in range(10**4)] * 10
    t = clock()
    unique( l )
    print "   ", round(clock()-t, 2)
    t = clock()
    unique( l, True )
    print "   ", round(clock()-t, 2)

    print "   with the brute force algorithm:"
    l = [[complex(e,e)] for e in range(3*10**2)] * 10
    t = clock()
    unique( l )
    print "   ", round(clock()-t, 2)
    t = clock()
    unique( l, True )
    print "   ", round(clock()-t, 2)
    print
