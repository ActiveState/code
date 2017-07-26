from math import frexp

class LF(object):
    """Long Float -- a class for high-precision floating point arithmetic.

    All arithmetic operations are exact except for division which has
    regular floating point precision.

    Construct with:
    * integers:  LF(10)
    * floats:    LF(math.pi)
    * tuples:    LF((323, -5))      # equal to 323 * 2.0 ** -5

    """

    __slots__ = ['mant', 'exp']     # long integer mantissa and int exponent

    def __new__(cls, value):
        if isinstance(value, LF):
            return value
        self = object.__new__(cls)
        if isinstance(value, tuple):
            mant, exp = value
            assert int(mant)==mant and int(exp)==exp
        else:
            mant, exp = frexp(value)
            mant, exp = int(mant * 2.0 ** 53), exp-53
        while mant and not mant & 1:
            mant >>= 1
            exp += 1
        self.mant, self.exp = mant, exp
        return self

    def __float__(self):
        return float(str(self.mant)) * 2.0 ** self.exp

    def __int__(self):
        m, e = self.mant, self.exp
        if e >= 0:
            value = m << e
        else:
            value = m >> -e
        return int(value)

    def __long__(self):
        return long(int(self))

    def __repr__(self):
        return '%s((%d, %d))' % (self.__class__.__name__, self.mant, self.exp)

    def __str__(self):
        return str(float(self))

    def _sync(self, other):
        other = LF(other)
        smant, sexp, omant, oexp = self.mant, self.exp, other.mant, other.exp
        if sexp < oexp:
            omant <<= oexp - sexp
            oexp = sexp
        else:
            smant <<= sexp - oexp
        return smant, omant, oexp

    def __add__(self, other):
        smant, omant, exp = self._sync(other)
        return LF((smant + omant, exp))

    def __radd__(self, other):
        return LF(self) + other

    def __sub__(self, other):
        smant, omant, exp = self._sync(other)
        return LF((smant - omant, exp))

    def __rsub__(self, other):
        return LF(self) - other

    def __mul__(self, other):
        other = LF(other)
        return LF((self.mant*other.mant, self.exp+other.exp))

    def __rmul__(self, other):
        return LF(self) * other

    def __cmp__(self, other):
        smant, omant, exp = self._sync(other)
        return cmp(smant, omant)

    def __hash__(self):
        return hash(float(self))

    def __pow__(self, b):
        assert b == int(b) and b >= 0
        return LF((self.mant ** b, self.exp * b))

    def __abs__(self):
        return LF((abs(self.mant), self.exp))

    def __pos__(self):
        return self

    def __neg__(self):
        return LF((-self.mant, self.exp))

    def __div__(self, other):
        return LF(float(self) / float(other))

    def __rdiv__(self, other):
        return LF(float(self) / float(other))

    def __nonzero__(self):
        return bool(self.mant)
