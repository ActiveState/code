def unzip(p, n):
    """Split a list-like object, 'p', into 'n' sub-lists by taking
    the next unused element of the main list and adding it to the
    next sub-list. A list of tuples (the sub-lists) is returned.
    Each of the sub-lists is of the same length; if p%n != 0, the
    shorter sub-lists are padded with 'None'.
        Example:
        >>> unzip(['a','b','c','d','e'], 3)
        [('a', 'd'), ('b', 'e'), ('c', None)]
    """
    (mlen, lft) = divmod(len(p),n)          # find length of longest sub-list
    if lft != 0: mlen += 1

    lst = [[None]*mlen for i in range(n)]   # initialize list of lists 
        
    for i in range(len(p)):
        (j, k) = divmod(i, n)
        lst[k][j] = p[i]

    return map(tuple, lst)
