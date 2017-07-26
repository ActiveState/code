def msum(iterable):
    "Full precision summation using multiple floats for intermediate values"
    # Rounded x+y stored in hi with the round-off stored in lo.  Together
    # hi+lo are exactly equal to x+y.  The inner loop applies hi/lo summation
    # to each partial so that the list of partial sums remains exact.
    # Depends on IEEE-754 arithmetic guarantees.  See proof of correctness at:
    # www-2.cs.cmu.edu/afs/cs/project/quake/public/papers/robust-arithmetic.ps

    partials = []               # sorted, non-overlapping partial sums
    for x in iterable:
        i = 0
        for y in partials:
            if abs(x) < abs(y):
                x, y = y, x
            hi = x + y
            lo = y - (hi - x)
            if lo:
                partials[i] = lo
                i += 1
            x = hi
        partials[i:] = [x]
    return sum(partials, 0.0)


from math import frexp

def lsum(iterable):
    "Full precision summation using long integers for intermediate values"
    # Transform (exactly) a float to m * 2 ** e where m and e are integers.
    # Adjust (tmant,texp) and (mant,exp) to make texp the common exponent.
    # Given a common exponent, the mantissas can be summed directly.

    tmant, texp = 0L, 0
    for x in iterable:
        mant, exp = frexp(x)
        mant, exp = long(mant * 2.0 ** 53), exp-53
        if texp > exp:
            tmant <<= texp - exp
            texp = exp
        else:
            mant <<= exp - texp
        tmant += mant
    return float(str(tmant)) * 2.0 ** texp

from itertools import imap

def lsum_26(iterable):
    "Full precision summation using long integers for intermediate values"
    # Py2.6 and later version of lsum() relying on float.as_integer_ratio().
    # Saves work by accumulating separate sums for each power-of-two 
    # denominator and then doing the bits shifts on the combined totals.
    fractions = {}
    fractions_get = fractions.get
    for n, d in imap(float.as_integer_ratio, iterable):
        fractions[d] = fractions_get(d, 0) + n
    tn, td = 0, 1
    for d, n in sorted(fractions.items()):
        while td < d:
            td <<= 1
            tn <<= 1
        tn += n
    return tn / td

from decimal import getcontext, Decimal, Inexact
getcontext().traps[Inexact] = True

def dsum(iterable):
    "Full precision summation using Decimal objects for intermediate values"
    # Transform (exactly) a float to m * 2 ** e where m and e are integers.
    # Convert (mant, exp) to a Decimal and add to the cumulative sum.
    # If the precision is too small for exact conversion and addition,
    # then retry with a larger precision.

    total = Decimal(0)
    for x in iterable:
        mant, exp = frexp(x)
        mant, exp = int(mant * 2.0 ** 53), exp-53
        while True:
            try:
                total += mant * Decimal(2) ** exp
                break
            except Inexact:
                getcontext().prec += 1
    return float(total)

from fractions import Fraction

def frsum(iterable):
    "Full precision summation using fractions for itermediate values"
    return float(sum(imap(Fraction.from_float, iterable)))


from random import random, gauss, shuffle

def test():
    for j in xrange(1000):
        vals = [7, 1e100, -7, -1e100, -9e-20, 8e-20] * 10
        s = 0
        for i in range(200):
            v = gauss(0, random()) ** 7 - s
            s += v
            vals.append(v)
        shuffle(vals)
        assert msum(vals) == lsum(vals) == dsum(vals) == frsum(vals) == lsum_26(vals)
        print '.',
    print 'Tests Passed'

if __name__ == '__main__':
    test()
