from itertools import islice, chain, repeat

def iterblocks(iterable, size, **kwds):
    '''Break an iterable into blocks of a given size.

    The optional keyword parameters determine the type of each block and what to
    do if the last block has smaller size (by default return it as is).

    @keyword blocktype: A callable f(iterable) for generating each block (tuple
        by default).
    @keyword truncate: If true, drop the last block if its length is less than
        `size`.
    @keyword pad: If given, the last block is padded with this object so that
        is length becomes equal to `size`.

    @returns: An iterator over blocks of the iterable.

    >>> list(iterblocks(xrange(7), 3))
    [(0, 1, 2), (3, 4, 5), (6,)]
    >>> list(iterblocks(xrange(7), 3, truncate=True))
    [(0, 1, 2), (3, 4, 5)]
    >>> list(iterblocks(xrange(7), 3, pad=None))
    [(0, 1, 2), (3, 4, 5), (6, None, None)]
    >>> list(iterblocks('abcdefg', 3, pad='-', blocktype=''.join))
    ['abc', 'def', 'g--']
    '''
    truncate = kwds.get('truncate',False)
    blocktype = kwds.get('blocktype',tuple)
    if truncate and 'pad' in kwds:
        raise ValueError("'truncate' must be false if 'pad' is given")
    iterator = iter(iterable)
    while True:
        block = blocktype(islice(iterator,size))
        if not block:
            break
        if len(block) < size:
            if 'pad' in kwds:
                block = blocktype(chain(block, repeat(kwds['pad'],
                                                      size-len(block))))
            elif truncate:
                break
        yield block
