"""
Continued fractions.
"""

from decimal import Decimal
from fractions import Fraction


class CFraction(list):
    """
    A continued fraction, represented as a list of integer terms.
    """

    def __init__(self, value, maxterms=15, cutoff=1e-10):
        if isinstance(value, (int, float, Decimal)):
            value = Decimal(value)
            remainder = int(value)
            self.append(remainder)

            while len(self) < maxterms:
                value -= remainder
                if value > cutoff:
                    value = Decimal(1) / value
                    remainder = int(value)
                    self.append(remainder)
                else:
                    break
        elif isinstance(value, (list, tuple)):
            self.extend(value)
        else:
            raise ValueError("CFraction requires number or list")

    def fraction(self, terms=None):
        "Convert to a Fraction."

        if terms is None or terms >= len(self):
            terms = len(self) - 1

        frac = Fraction(1, self[terms])
        for t in reversed(self[1:terms]):
            frac = 1 / (frac + t)

        frac += self[0]
        return frac

    def __float__(self):
        return float(self.fraction())

    def __str__(self):
        return "[%s]" % ", ".join([str(x) for x in self])

if __name__ == "__main__":
    from math import e, pi, sqrt

    numbers = {
        "phi": (1 + sqrt(5)) / 2,
        "pi": pi,
        "e": e,
    }

    print "Continued fractions of well-known numbers"
    for name, value in numbers.items():
        print "   %-8s  %r" % (name, CFraction(value))

    for name, value in numbers.items():
        print
        print "Approximations to", name
        cf = CFraction(value)
        for t in xrange(len(cf)):
            print "   ", cf.fraction(t)

    print
    print "Some irrational square roots"
    for n in 2, 3, 5, 6, 7, 8:
        print "   ", "sqrt(%d)  %r" % (n, CFraction(sqrt(n)))

    print
    print "Decimals from 0.1 to 0.9"
    for n in xrange(1, 10):
        cf = CFraction(n / 10.0)
        print "   ", float(cf), cf
