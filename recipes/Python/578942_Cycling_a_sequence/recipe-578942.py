def cycle(seq):
    """Return a generator producing items from seq. When seq is
    exhausted, the generator will cycle over from item 0 again.

    Beware that a break statement is necessary in a for loop. Also, seq
    is a sequence supporting the len function and enumerated 0-based.

    Examples:

    >>> seq = ['one', 'two', 'three']
    >>> cyc = cycle(seq)
    >>> next(cyc)
    'one'
    >>> next(cyc)
    'two'
    >>> next(cyc)
    'three'
    >>> next(cyc)
    'one'
    >>> next(cyc)
    'two'

    To reset, call for a new cycle:

    >>> cyc = cycle(seq)
    >>> next(cyc)
    'one'
    >>> for i, item in enumerate(cyc):
    ...     print i, item
    ...     if i > 3:
    ...         break # Must break out manually
    ... 
    0 two
    1 three
    2 one
    3 two
    4 three

    """
    i = 0
    while True:                 # Cycle forever
        yield seq[i]
        i = (i + 1) % len(seq)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
