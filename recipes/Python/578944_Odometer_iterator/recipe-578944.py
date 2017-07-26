def odometer(syms=range(10), rolls=2, start=0, stop=None):
    """
    Logic exercise. For each roll, if the previous roll rolled over,
    roll the roll.

    The range of "values" is defined by syms, it is a list with any
    objects. Yield all possible combinations being len(syms)**rolls.

    Examples:

    >>> Hex = range(10) + ['A', 'B', 'C', 'D', 'E', 'F']
    >>> odo = odometer(Hex, stop=16)
    >>> for om in odo:
    ...     print om
    ... 
    [0, 0]
    [0, 1]
    [0, 2]
    [0, 3]
    [0, 4]
    [0, 5]
    [0, 6]
    [0, 7]
    [0, 8]
    [0, 9]
    [0, 'A']
    [0, 'B']
    [0, 'C']
    [0, 'D']
    [0, 'E']
    [0, 'F']
    >>> odo = odometer(Hex, start=250, stop=256)
    >>> for om in odo:
    ...     print om
    ... 
    ['F', 'A']
    ['F', 'B']
    ['F', 'C']
    ['F', 'D']
    ['F', 'E']
    ['F', 'F']
    >>> odo = odometer(['haz', 'the', 'code'], rolls=3)
    >>> fmt = '{} {} {}?'
    >>> for om in odo:
    ...     print fmt.format(om[0].capitalize(), *om[1:])
    ... 
    Haz haz haz?
    Haz haz the?
    Haz haz code?
    Haz the haz?
    Haz the the?
    Haz the code?
    Haz code haz?
    Haz code the?
    Haz code code?
    The haz haz?
    The haz the?
    The haz code?
    The the haz?
    The the the?
    The the code?
    The code haz?
    The code the?
    The code code?
    Code haz haz?
    Code haz the?
    Code haz code?
    Code the haz?
    Code the the?
    Code the code?
    Code code haz?
    Code code the?
    Code code code?

    """
    
    base = len(syms)
    combinations = base**rolls

    # The odometer is to be reversed on delivery.
    odo = [syms[0] for i in range(rolls)]

    # Odometer start setting:
    curval = start
    for i in range(rolls):
        j = curval % base
        odo[i] = syms[j]
        curval = curval // base

    curval = start
    while curval < (stop or combinations):
        # Consider roll 0 to be rightmost.
        yield odo[-1::-1]
        for roll, sym in enumerate(odo[:]):
            i = syms.index(sym)
            if i < base - 1:
                odo[roll] = syms[i + 1]
                # Could roll the roll w/o roll-over, next value:
                break
            else:
                odo[roll] = syms[0]
                # There was a roll-over, next roll.
        curval += 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()
