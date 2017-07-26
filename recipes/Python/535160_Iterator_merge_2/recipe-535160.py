def itermerge( *iters ):
    '''Merge multiple sorted inputs into a single sorted output.

    Equivalent to:  sorted(itertools.chain(*iterables))

    >>> list(imerge([1,3,5,7], [0,2,4,8], [5,10,15,20], [], [25]))
    [0, 1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]

    '''

    def merge( i1, i2 ):
        next1 = iter( i1 ).next
        next2 = iter( i2 ).next
        try:        
            v1 = next1()
        except StopIteration:
            while True:
                yield next2()
        try:
            v2 = next2()
        except StopIteration:
            while True:
                yield next1()
        while True:
            if v1 < v2:
                yield v1
                try:        
                    v1 = next1()
                except StopIteration:
                    yield v2
                    while True:
                        yield next2()
            else:
                yield v2
                try:
                    v2 = next2()
                except StopIteration:
                    yield v1
                    while True:
                        yield next1()
    iters_cnt = len( iters )
    if iters_cnt == 1:
        return iter( iters[0] )
    if iters_cnt == 2:
        return merge( iters[0], iters[1] )
    bisect = iters_cnt / 2
    return merge( itermerge( *iters[:bisect] ), itermerge( *iters[bisect:] ) )
if __name__ == '__main__':
    import doctest
    import itertools
    import heapq
    import random
    from timeit import Timer
    def test_data( dataset_cnt=5, sizerange=(100, 100) ):
        print ( "%s sets between %s and %s"
                    % ( dataset_cnt, sizerange[0], sizerange[1] ) )
        datasets = []
        for li in xrange( dataset_cnt ):
            d = []
            for i in xrange( int( random.uniform( *sizerange ) ) ):
                d.append( int( random.uniform( 0, 99 ) ) )
            d.sort()
            datasets.append( d )
        return tuple( datasets )

    def isort( *iters ):
        return iter( sorted( itertools.chain( *iters ) ) )


    #
    # From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/491285
    #  for comparison
    #


    def imerge(*iterables):
        '''Merge multiple sorted inputs into a single sorted output.

        Equivalent to:  sorted(itertools.chain(*iterables))

        >>> list(imerge([1,3,5,7], [0,2,4,8], [5,10,15,20], [], [25]))
        [0, 1, 2, 3, 4, 5, 5, 7, 8, 10, 15, 20, 25]

        '''
        heappop, siftup, _StopIteration = heapq.heappop, heapq._siftup, StopIteration

        h = []
        h_append = h.append
        for it in map(iter, iterables):
            try:
                next = it.next
                h_append([next(), next])
            except _StopIteration:
                pass
        heapq.heapify(h)

        while 1:
            try:
                while 1:
                    v, next = s = h[0]      # raises IndexError when h is empty
                    yield v
                    s[0] = next()           # raises StopIteration when exhausted
                    siftup(h, 0)            # restore heap condition
            except _StopIteration:
                heappop(h)                  # remove empty iterator
            except IndexError:
                return
    #
    #  End
    #
    datasets = test_data( 10, ( 1, 10000 ) )
    verify_result = list( itertools.chain( *datasets ) )
    verify_result.sort()
    test_cnt = 3
    print "%s tests per timing run" % test_cnt

    def test( what ):
        name = what.__name__
        print name," "
        if list( what( *datasets ) ) == verify_result:
            print "Success!!"
        else:
            print "failure"
            return
        set_up = "from __main__ import %s, datasets; gc.enable()" % name
        test_it = "list( %s( *datasets ) )" % name
        print Timer( test_it, set_up ).timeit( test_cnt )

    test( isort )
    test( itermerge )
    test( imerge )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
