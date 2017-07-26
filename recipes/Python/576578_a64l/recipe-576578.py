def a64l(s):
    """
    An implementation of a64l as from the c stdlib.
    Convert between a radix-64 ASCII string and a 32-bit integer.

    '.' (dot) for 0, '/' for 1, '0' through '9' for [2,11],
    'A' through 'Z' for [12,37], and 'a' through 'z' for [38,63].

    TODO:
        do some implementations use '' instead of '.' for 0?

    >>> a64l('.')
    0
    >>> a64l('ZZZZZZ')
    40359057765L
    #only the first 6 chars are significant
    >>> a64l('ZZZZZZ.')
    40359057765L
    >>> a64l('A')
    12
    >>> a64l('Chris')
    951810894
    """
    MASK = 0xffffffff
    BITSPERCHAR = 6
    orda, ordZ, ordA, ord9, ord0 = ord('a'), ord('Z'), ord('A'), ord('9'), ord('0')

    r = 0
    for shift, c in enumerate(s[:6]):
        c = ord(c)
        if c > ordZ:
            c -= orda - ordZ - 1
        if c > ord9:
            c -= ordA - ord9 - 1
        r = (r | ((c - (ord0 - 2)) << (shift * BITSPERCHAR))) & MASK
    return r
