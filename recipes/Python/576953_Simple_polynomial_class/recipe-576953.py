"""\
This class implements polynomial functions over a single variable. It
represents the polynomial as a list of numbers and allows most
arithmetic operations, using conventional Python syntax. It does not
do symbolic manipulations. Instead, you can do things like this:

>>> x = SimplePolynomial()
>>> quadratic = (x+1)*(x-1)
>>> str(quadratic)
'X**2 - 1'
>>> quadratic(4)
15
>>> for i in range(4):
...     polynomial = (x+1)**i
...     i, str(polynomial), polynomial(1)
(0, '1', 1)
(1, 'X + 1', 2)
(2, 'X**2 + 2*X + 1', 4)
(3, 'X**3 + 3*X**2 + 3*X + 1', 8)
"""

from __future__ import division, generators

from operator import add

try:
    from itertools import izip_longest
except ImportError:
    # The izip_longest function was added in version 2.6
    # If we can't find it, use an equivalent implementation.
    from itertools import chain, repeat
    class ZipExhausted(Exception):
        pass
    def izip_longest(*args, **kwds):
        # izip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
        fillvalue = kwds.get('fillvalue')
        counter = [len(args) - 1]
        def sentinel():
            if not counter[0]:
                raise ZipExhausted
            counter[0] -= 1
            yield fillvalue
        fillers = repeat(fillvalue)
        iterators = [chain(it, sentinel(), fillers) for it in args]
        try:
            while iterators:
                yield tuple(map(next, iterators))
        except ZipExhausted:
            pass

try:
    from numbers import Number
except ImportError:
    # The numbers module was added in version 2.6
    # If we can't find it, use an equivalent implementation.
    Number = (int, float, long, complex)


class SimplePolynomial(object):

    def __init__(self, terms=[0,1]):
        """\
>>> str(SimplePolynomial())
'X'
"""
        try:
            while terms[-1] == 0:
                del terms[-1]
        except IndexError:
            pass
        self.terms = list(terms)

    def __str__(self):
        """\
Needs some work, but adequate.
"""
        l = len(self.terms)
        if l == 0:
            return '0'
        if l == 1:
            return str(self.terms[0])
        result = []
        for i, c in reversed(list(enumerate(self.terms))):
            if c == 0:
                continue
            if c < 0:
                result.append('-')
                c = - c
            else:
                result.append('+')
                
            if c == 1:
                if i == 0:
                    result.append('1')
                elif i == 1:
                    result.append('X')
                else:
                    result.append('X**%g' % i)
            else:
                if i == 0:
                    result.append('%g' % c)
                elif i == 1:
                    result.append('%g*X' % c)
                else:
                    result.append('%g*X**%d' % (c, i))
        if len(result) == 0:
            return '0'
        if result[0] == '-':
            result[1] = '-'+result[1]
        del result[0]
        return ' '.join(result)

    def __add__(self, other):
        """\
>>> str(SimplePolynomial() + 1)
'X + 1'
>>> str(1 + SimplePolynomial())
'X + 1'
>>> str(SimplePolynomial() + SimplePolynomial())
'2*X'
"""
        if len(self.terms) == 0:
            return other
        if isinstance(other, Number):
            terms = self.terms[:]
            terms[0] += other
            return SimplePolynomial(terms)
        return SimplePolynomial([
            add(*pair)
            for pair in izip_longest(self.terms, other.terms, fillvalue=0)
            ])

    # Since addition is commutative, reuse __add__
    __radd__ = __add__

    def __neg__(self):
        """\
>>> str(- SimplePolynomial())
'-X'
"""
        return SimplePolynomial([-c for c in self.terms])

    def __sub__(self, other):
        """\
>>> str(SimplePolynomial() - 1)
'X - 1'
>>> str(SimplePolynomial() - SimplePolynomial())
'0'
"""
        return self + -other

    def __rsub__(self, other):
        """\
>>> str(1 - SimplePolynomial())
'-X + 1'
"""
        return -self + other

    def __mul__(self, other):
        """\
>>> str(SimplePolynomial() * 2)
'2*X'
>>> str(2 * SimplePolynomial())
'2*X'
>>> str(SimplePolynomial() * SimplePolynomial())
'X**2'
"""
        if isinstance(other, Number):
            return SimplePolynomial([c * other for c in self.terms])
        terms = [0]*(len(self.terms)+len(other.terms))
        for i1, c1 in enumerate(self.terms):
            for i2, c2 in enumerate(other.terms):
                terms[i1+i2] += c1*c2
        return SimplePolynomial(terms)

    # Since multiplication is commutative, reuse __mul__
    __rmul__ = __mul__

    def __truediv__(self, other):
        """\
Implements some simple forms of division.  See
http://en.wikipedia.org/wiki/Synthetic_division
for details.

>>> str(SimplePolynomial() / 2)
'0.5*X'
>>> x = SimplePolynomial()
>>> quotient, remainder  = (x**3 - 12*x**2 - 42) / (x - 3)
>>> str(quotient), str(remainder)
('X**2 - 9*X - 27', '-123')
"""
        if isinstance(other, Number):
            return SimplePolynomial([c / other for c in self.terms])
        if len(other.terms) == 1:
            return self/other.terms[0]
        assert len(other.terms) == 2
        dividend = self.terms[:]
        divisor = other.terms[:]
        assert divisor[-1] == 1
        xi = 0
        result = []
        for i in xrange(-1, -len(dividend) - 1, -1):
            xi = dividend[i] - xi * divisor[0]
            result.insert(0, xi)
        return SimplePolynomial(result[1:]), result[0]
        raise NotImplementedError('synthetic division')

    __div__ = __truediv__

    def __eq__(self, other):
        """\
>>> SimplePolynomial() == SimplePolynomial()
True
>>> SimplePolynomial() - SimplePolynomial() == 0
True
"""
        if isinstance(other, SimplePolynomial):
            return self.terms == other.terms
        if isinstance(other, Number):
            if len(self.terms) > 1:
                return False
            try:
                self.terms[0] == other
            except IndexError:
                return other == 0
        return False

    def __ne__(self, other):
        return not self == other

    def copy(self):
        return SimplePolynomial(self.terms[:])

    def __pow__(self, exponent):
        """\
Uses the Russian Peasant Multiplication algorithm.

>>> str(SimplePolynomial() ** 2)
'X**2'
>>> str(SimplePolynomial() ** 0.5)
Traceback (most recent call last):
...
NotImplementedError: exponent is not an integer
>>> str(SimplePolynomial() ** -1)
Traceback (most recent call last):
...
NotImplementedError: exponent is less than zero
"""
        if not isinstance(exponent, int):
            raise NotImplementedError('exponent is not an integer')
        if exponent < 0:
            raise NotImplementedError('exponent is less than zero')
        tmp = self.copy()
        result = SimplePolynomial([1])
        while exponent > 0:
            if exponent & 1:
                result *= tmp
            tmp *= tmp
            exponent >>= 1
        return result

    def __call__(self, x):
        """\
Evaluate the polynomial for the given value using the Horner scheme.

>>> SimplePolynomial()(1)
1
"""
        result = 0
        for c in reversed(self.terms):
            result = result * x + c
        return result

    def derivative(self):
        """\
>>> str(SimplePolynomial().derivative())
'1'
"""
        terms = [i*c for i, c in enumerate(self.terms)]
        return SimplePolynomial(terms[1:])

    def integrate(self, const=0):
        """\
>>> str(SimplePolynomial().integrate())
'0.5*X**2'
"""
        terms = [const]
        terms.extend([c/(i+1) for i, c in enumerate(self.terms)])
        return SimplePolynomial(terms)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
