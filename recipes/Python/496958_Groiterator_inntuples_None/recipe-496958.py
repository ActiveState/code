from itertools import *
def group(lst, n):
    """group([0,3,4,10,2,3], 2) => iterator
    
    Group an iterable into an n-tuples iterable. Incomplete tuples
    are padded with Nones e.g.
    
    >>> list(group(range(10), 3))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]
    """
    iters = tee(lst, n)
    iters = [iters[0]] + [chain(iter, repeat(None))  
                 for iter in iters[1:]]
    return izip(
         *[islice(iter, i, None, n) for i, iter 
              in enumerate(iters)])
