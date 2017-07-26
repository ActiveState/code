def A001511():
    '''Sequence of moves to solve Towers of Hanoi; has many other interpretations.
For more info see http://www.research.att.com/projects/OEIS?Anum=A001511'''
    yield 1
    for x in A001511():
        yield x+1
        yield 1

def A003714():
    '''Fibbinary numbers (no consecutive ones in binary representation).
For more info see http://www.research.att.com/projects/OEIS?Anum=A003714'''
    yield 1
    for x in A003714():
        yield 2*x
        if not (x & 1):
            yield 2*x+1

def A005836():
    '''Numbers with no 2 in their ternary representation; discrete Cantor set;
lexicographically first arithmetic-progression-free sequence of integers.
For more info see http://www.research.att.com/projects/OEIS?Anum=A005836'''

    yield 0
    for x in A005836():
        if x:
            yield 3*x
        yield 3*x+1

def A006068():
    '''Inverse Gray code; each n occurs at position n^(n>>1) of the sequence.
For more info see http://www.research.att.com/projects/OEIS?Anum=A006068'''
    yield 0
    for x in A006068():
        if x & 1:
            yield 2*x+1
            yield 2*x
        else:
            if x:
                yield 2*x
            yield 2*x+1

def A010060():
    '''Thue-Morse sequence; binary sequence with no triply-repeated block.
For more info see http://www.research.att.com/projects/OEIS?Anum=A010060'''
    yield 0
    omit = 1
    for x in A010060():
        if x:
            yield 1
            yield 0
        else:
            if not omit:
                yield 0
            yield 1
        omit = 0

def A036561():
    '''Numbers of the form 2^i 3^j, sorted according to the order of the tuples (i+j,j).
For more info see http://www.research.att.com/projects/OEIS?Anum=A036561'''
    yield 1
    for x in A036561():
        yield 2*x
        if x & 1:
            yield 3*x
