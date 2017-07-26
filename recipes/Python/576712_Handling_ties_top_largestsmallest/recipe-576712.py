import heapq, bisect
from operator import itemgetter, neg
from itertools import islice, repeat, count, imap, izip, tee


def nlargest(n, iterable, key=None, ties=False):
    '''Find the n largest elements in iterable.
    
    @param ties: If False, equivalent to heapq.nlargest(); ties are not taken
        into account. If True, the returned list is guaranteed to contain all
        the equal smallest elements of the top-`n`. If it is not possible to
        satisfy this constraint by returning a list of size `n` exactly, then
        the top-`k` elements that satisfy the constraint are returned, where
        `k` is the largest integer smaller than `n`.
        
    >>> s = [-4,3,5,7,4,-7,-4,-3]
    >>> for i in xrange(1,len(s)+1):
    ...     print i, nlargest(i,s,key=abs)
    1 [7]
    2 [7, -7]
    3 [7, -7, 5]
    4 [7, -7, 5, -4]
    5 [7, -7, 5, -4, 4]
    6 [7, -7, 5, -4, 4, -4]
    7 [7, -7, 5, -4, 4, -4, 3]
    8 [7, -7, 5, -4, 4, -4, 3, -3]

    >>> for i in xrange(1,len(s)+1):
    ...     print i, nlargest(i,s,key=abs,ties=True)
    1 []
    2 [7, -7]
    3 [7, -7, 5]
    4 [7, -7, 5]
    5 [7, -7, 5]
    6 [7, -7, 5, -4, 4, -4]
    7 [7, -7, 5, -4, 4, -4]
    8 [7, -7, 5, -4, 4, -4, 3, -3]
    '''
    if not ties:
        return heapq.nlargest(n, iterable, key)
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), imap(neg, count()), in2)      # decorate
    result = list(islice(it, n))
    if not result:
        return result
    heapq.heapify(result)    
    heappush, heappop, heapreplace = heapq.heappush, heapq.heappop, heapq.heapreplace
    # smallest_key: smallest key of the nlargest
    smallest_key = result[0][0]
    # overflow: True if there are currently ties that don't fit in result
    overflow = False    
    for elem in it:        
        elem_key = elem[0]
        if elem_key < smallest_key:
            continue
        if not overflow:
            assert len(result) == n and result[0][0] == smallest_key
            if elem_key > smallest_key:
                elem_key = heapreplace(result, elem)[0]
                smallest_key = result[0][0]
            assert elem_key <= smallest_key
            # if the pending element (new or replaced) is equal to the smallest
            # we've got a tie that can't fit in result: drop ties
            if elem_key == smallest_key:
                overflow = True
                while result and result[0][0] == elem_key:
                    heappop(result)
        else:
            assert len(result) < n
            if elem_key > smallest_key:
                heappush(result, elem)
                if len(result) == n:
                    # result just filled and the last element is larger
                    # than smallest: existing ties are invalidated
                    overflow = False
                    smallest_key = result[0][0]
    result.sort(reverse=True)
    return map(itemgetter(2), result)                       # undecorate 


def nsmallest(n, iterable, key=None, ties=False):
    '''Find the n smallest elements in iterable.
    
    @param ties: If False, equivalent to heapq.nsmallest(); ties are not taken
        into account. If True, the returned list is guaranteed to contain all
        the equal largest elements of the top-`n`. If it is not possible to
        satisfy this constraint by returning a list of size `n` exactly, then
        the top-`k` elements that satisfy the constraint are returned, where
        `k` is the largest integer smaller than `n`.
        
    >>> s = [-4,3,5,7,4,-7,-4,-3]
    >>> for i in xrange(1,len(s)+1):
    ...     print i, nsmallest(i,s,key=abs)
    1 [3]
    2 [3, -3]
    3 [3, -3, -4]
    4 [3, -3, -4, 4]
    5 [3, -3, -4, 4, -4]
    6 [3, -3, -4, 4, -4, 5]
    7 [3, -3, -4, 4, -4, 5, 7]
    8 [3, -3, -4, 4, -4, 5, 7, -7]

    >>> for i in xrange(1,len(s)+1):
    ...     print i, nsmallest(i,s,key=abs,ties=True)
    1 []
    2 [3, -3]
    3 [3, -3]
    4 [3, -3]
    5 [3, -3, -4, 4, -4]
    6 [3, -3, -4, 4, -4, 5]
    7 [3, -3, -4, 4, -4, 5]
    8 [3, -3, -4, 4, -4, 5, 7, -7]
    '''
    if not ties:
        return heapq.nsmallest(n, iterable, key)
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), count(), in2)     # decorate
    if hasattr(iterable, '__len__') and n * 10 <= len(iterable):
        # For smaller values of n, the bisect method is faster than a minheap.
        # It is also memory efficient, consuming only n elements of space.
        result = sorted(islice(it, n))
        if not result:
            return []
        insort = bisect.insort
        pop = result.pop
        # largest_key: largest key of the nsmallest
        largest_key = result[-1][0]
        # overflow: True if there are currently ties that don't fit in result
        overflow = False
        for elem in it:
            elem_key = elem[0]
            if elem_key > largest_key:
                continue
            if not overflow:
                assert len(result) == n and result[-1][0] == largest_key
                if elem_key < largest_key:
                    insort(result, elem)
                    # pop the largest from the result
                    elem_key = pop()[0]
                    # and update largest to the new largest
                    largest_key = result[-1][0]
                assert elem_key >= largest_key
                # if the pending element (new or popped) is equal to the largest
                # we've got a tie that can't fit in result: drop ties
                if elem_key == largest_key:
                    overflow = True
                    while result and result[-1][0] == elem_key:
                        pop()
            else:
                assert len(result) < n
                if elem_key < largest_key:
                    insort(result, elem)
                    if len(result) == n:
                        # result just filled and the last element is smaller
                        # than largest: existing ties are invalidated
                        overflow = False
                        largest_key = result[-1][0]
    else:
        # An alternative approach manifests the whole iterable in memory but
        # saves comparisons by heapifying all at once.  Also, saves time
        # over bisect.insort() which has O(n) data movement time for every
        # insertion.  Finding the n smallest of an m length iterable requires
        #    O(m) + O(n log m) comparisons.
        h = list(it)
        heapq.heapify(h)
        result = map(heapq.heappop, repeat(h, min(n, len(h))))
        if result:
            largest_key = result[-1][0]
            # is largest_key equal to the next smallest in heap ?
            if h and h[0][0] == largest_key:
                # if yes, delete all trailing ties
                while result and result[-1][0] == largest_key:
                    del result[-1]
    return map(itemgetter(2), result)     # undecorate 


if __name__ == '__main__':    
    import doctest; doctest.testmod()
