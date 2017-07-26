def letter2num(letters, zbase=False):
    """A = 1, C = 3 and so on. Convert spreadsheet style column
    enumeration to a number.

    Answers:
    A = 1, Z = 26, AA = 27, AZ = 52, ZZ = 702, AMJ = 1024

    >>> letter2num('A') == 1
    True
    >>> letter2num('Z') == 26
    True
    >>> letter2num('AZ') == 52
    True
    >>> letter2num('ZZ') == 702
    True
    >>> letter2num('AMJ') == 1024
    True
    >>> letter2num('AMJ', zbase=True) == 1023
    True
    >>> letter2num('A', zbase=True) == 0
    True

    """

    letters = letters.upper()
    res = 0
    weight = len(letters) - 1
    for i, c in enumerate(letters):
        res += (ord(c) - 64) * 26**(weight - i)
    if not zbase:
        return res
    return res - 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()
