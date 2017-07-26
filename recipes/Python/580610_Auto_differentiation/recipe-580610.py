'Toolkit for automatic-differentiation of Python functions'

# Resources for automatic-differentiation:
# https://en.wikipedia.org/wiki/Automatic_differentiation
# https://justindomke.wordpress.com/2009/02/17/
# http://www.autodiff.org/

from __future__ import division
import math

##  Dual Number Class  #####################################################

class Num(float):
    ''' The auto-differentiation number class works likes a float
        for a function input, but all operations on that number
        will concurrently compute the derivative.

        Creating Nums
        -------------
        New numbers are created with:  Num(x, dx)
        Make constants (not varying with respect to x) with:  Num(3.5)
        Make variables (that vary with respect to x) with:  Num(3.5, 1.0)
        The short-cut for Num(3.5, 1.0) is:  Var(3.5)

        Accessing Nums
        --------------
        Convert a num back to a float with:  float(n)
        The derivative is accessed with:  n.dx
        Or with a the short-cut function:  d(n)

        Functions of One Variable
        -------------------------
        >>> f = lambda x:  cos(2.5 * x) ** 3
        >>> y = f(Var(1.5))                     # Evaluate at x=1.5
        >>> y                                   # f(1.5)
        -0.552497105486732
        >>> y.dx                                # f'(1.5)
        2.88631746797551

        Partial Derivatives and Gradients of Multi-variable Functions
        -------------------------------------------------------------

        The tool can also be used to compute gradients of multivariable
        functions by making one of the inputs variable and the keeping
        the remaining inputs constant:

        >>> f = lambda x, y:  x*y + sin(x)
        >>> f(2.5, 3.5)                         # Evaluate at (2.5, 3.5)
        9.348472144103956
        >>> d(f(Var(2.5), 3.5))                 # Partial with respect to x
        2.6988563844530664
        >>> d(f(2.5, Var(3.5)))                 # Partial with respect to y
        2.5
        >>> gradient(f, (2.5, 3.5))
        (2.6988563844530664, 2.5)

        See:  https://www.wolframalpha.com/input/?lk=3&i=grad(x*y+%2B+sin(x))

    '''
    # Tables of Derivatives:
    # http://hyperphysics.phy-astr.gsu.edu/hbase/math/derfunc.html
    # http://tutorial.math.lamar.edu/pdf/Common_Derivatives_Integrals.pdf
    # http://www.nps.edu/Academics/Schools/GSEAS/Departments/Math/pdf_sources/BlueBook27.pdf
    # https://www.wolframalpha.com/input/?lk=3&i=d%2Fdx(u(x)%5E(v(x)))

    __slots__ = ['dx']

    def __new__(cls, value, dx=0.0):
        if isinstance(value, cls): return value
        inst = float.__new__(cls, value)
        inst.dx = dx
        return inst

    def __add__(u, v):
        return Num(float(u) + float(v), d(u) + d(v))

    def __sub__(u, v):
        return Num(float(u) - float(v), d(u) - d(v))

    def __mul__(u, v):
        u, v, du, dv = float(u), float(v), d(u), d(v)
        return Num(u * v, u * dv + v * du)

    def __truediv__(u, v):
        u, v, du, dv = float(u), float(v), d(u), d(v)
        return Num(u / v, (v * du - u * dv) / v ** 2.0)

    def __pow__(u, v):
        u, v, du, dv = float(u), float(v), d(u), d(v)
        return Num(u ** v,
                   (v * u ** (v - 1.0) * du  if du else 0.0) +
                   (math.log(u) * u ** v * dv if dv else 0.0))

    def __floordiv__(u, v):
        return Num(float(u) // float(v), 0.0)

    def __mod__(u, v):
        u, v, du, dv = float(u), float(v), d(u), d(v)
        return Num(u % v, du - u // v * dv)

    def __pos__(u):
        return u

    def __neg__(u):
        return Num(-float(u), -d(u))

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return -(self - other)

    def __rtruediv__(self, other):
        return Num(other) / self

    def __rpow__(self, other):
        return Num(other) ** self

    def __rmod__(u, v):
        return Num(v) % u

    def __rfloordiv__(self, other):
        return Num(other) // self

    def __abs__(self):
        return self if self >= 0.0 else -self

##  Convenience Functions  #################################################
Var = lambda x: Num(x, 1.0)
d = lambda x: getattr(x, 'dx', 0.0)

##  Math Module Functions and Constants  ###################################
sqrt = lambda u: Num(math.sqrt(u), d(u) / (2.0 * math.sqrt(u)))
log = lambda u: Num(math.log(u), d(u) / float(u))
log2 = lambda u: Num(math.log2(u), d(u) / (float(u) * math.log(2.0)))
log10 = lambda u: Num(math.log10(u), d(u) / (float(u) * math.log(10.0)))
log1p = lambda u: Num(math.log1p(u), d(u) / (float(u) + 1.0))
exp = lambda u: Num(math.exp(u), math.exp(u) * d(u))
expm1 = lambda u: Num(math.expm1(u), math.exp(u) * d(u))
sin = lambda u: Num(math.sin(u), math.cos(u) * d(u))
cos = lambda u: Num(math.cos(u), -math.sin(u) * d(u))
tan = lambda u: Num(math.tan(u), d(u) / math.cos(u) ** 2.0)
sinh = lambda u: Num(math.sinh(u), math.cosh(u) * d(u))
cosh = lambda u: Num(math.cosh(u), math.sinh(u) * d(u))
tanh = lambda u: Num(math.tanh(u), d(u) / math.cosh(u) ** 2.0)
asin = lambda u: Num(math.asin(u), d(u) / math.sqrt(1.0 - float(u) ** 2.0))
acos = lambda u: Num(math.acos(u), -d(u) / math.sqrt(1.0 - float(u) ** 2.0))
atan = lambda u: Num(math.atan(u), d(u) / (1.0 + float(u) ** 2.0))
asinh = lambda u: Num(math.asinh(u), d(u) / math.hypot(u, 1.0))
acosh = lambda u: Num(math.acosh(u), d(u) / math.sqrt(float(u) ** 2.0 - 1.0))
atanh = lambda u: Num(math.atanh(u), d(u) / (1.0 - float(u) ** 2.0))
radians = lambda u: Num(math.radians(u), math.radians(d(u)))
degrees = lambda u: Num(math.degrees(u), math.degrees(d(u)))
erf = lambda u: Num(math.erf(u),
                    2.0 / math.sqrt(math.pi) * math.exp(-(float(u) ** 2.0)) * d(u))
erfc = lambda u: Num(math.erfc(u),
                    -2.0 / math.sqrt(math.pi) * math.exp(-(float(u) ** 2.0)) * d(u))
hypot = lambda u, v: Num(math.hypot(u, v),
                         (u * d(u) + v * d(v)) / math.hypot(u, v))
fsum = lambda u: Num(math.fsum(map(float, u)), math.fsum(map(d, u)))
fabs = lambda u: abs(Num(u))
fmod = lambda u, v: Num(u) % v
copysign = lambda u, v: Num(math.copysign(u, v),
            d(u) if math.copysign(1.0, float(u) * float(v)) > 0.0  else -d(u))
ceil = lambda u: Num(math.ceil(u), 0.0)
floor = lambda u: Num(math.floor(u), 0.0)
trunc = lambda u: Num(math.trunc(u), 0.0)
pi = Num(math.pi)
e = Num(math.e)

##  Backport Python 3 Math Module Functions  ###############################

if not hasattr(math, 'isclose'):
    math.isclose = lambda x, y, rel_tol=1e-09: abs(x/y - 1.0) <= rel_tol

if not hasattr(math, 'log2'):
    math.log2 = lambda x: math.log(x) / math.log(2.0)

##  Vector Functions  ######################################################

def partial(func, point, index):
    ''' Partial derivative at a given point

        >>> func = lambda x, y:  x*y + sin(x)
        >>> point = (2.5, 3.5)
        >>> partial(func, point, 0)             # Partial with respect to x
        2.6988563844530664
        >>> partial(func, point, 1)             # Partial with respect to y
        2.5

    '''
    return d(func(*[Num(x, i==index) for i, x in enumerate(point)]))

def gradient(func, point):
    ''' Vector of the partial derivatives of a scalar field

        >>> func = lambda x, y:  x*y + sin(x)
        >>> point = (2.5, 3.5)
        >>> gradient(func, point)
        (2.6988563844530664, 2.5)

        See:  https://www.wolframalpha.com/input/?lk=3&i=grad(x*y+%2B+sin(x))

    '''
    return tuple(partial(func, point, index) for index in range(len(point)))

def directional_derivative(func, point, direction):
    ''' The dot product of the gradient and a direction vector.
        Computed directly with a single function call.

        >>> func = lambda x, y:  x*y + sin(x)
        >>> point = (2.5, 3.5)
        >>> direction = (1.5, -2.2)
        >>> directional_derivative(func, point, direction)
        -1.4517154233204006

        Same result as separately computing and dotting the gradient:
        >>> math.fsum(g * d for g, d in zip(gradient(func, point), direction))
        -1.4517154233204002

        See:  https://en.wikipedia.org/wiki/Directional_derivative

    '''
    return d(func(*map(Num, point, direction)))

def divergence(F, point):
    ''' Sum of the partial derivatives of a vector field

        >>> F = lambda x, y, z: (x*y+sin(x)+3*x, x-y-5*x, cos(2*x)-sin(y)**2)
        >>> divergence(F, (3.5, 2.1, -3.3))
        3.163543312709203

        # http://www.wolframalpha.com/input/?i=div+%7Bx*y%2Bsin(x)%2B3*x,+x-y-5*x,+cos(2*x)-sin(y)%5E2%7D
        >>> x, y, z = (3.5, 2.1, -3.3)
        >>> math.cos(x) + y + 2
        3.1635433127092036

        >>> F = lambda x, y, z: (8 * exp(-x), cosh(z), - y**2)
        >>> divergence(F, (2, -1, 4))
        -1.0826822658929016

        # https://www.youtube.com/watch?v=S2rT2zK2bdo
        >>> x, y, z = (2, -1, 4)
        >>> -8 * math.exp(-x)
        -1.0826822658929016

    '''
    return math.fsum(d(F(*[Num(x, i==index) for i, x in enumerate(point)])[index])
                     for index in range(len(point)))

def curl(F, point):
    ''' Rotation around a vector field

        >>> F = lambda x, y, z: (x*y+sin(x)+3*x, x-y-5*x, cos(2*x)-sin(y)**2)
        >>> curl(F, (3.5, 2.1, -3.3))
        (0.8715757724135881, 1.3139731974375781, -7.5)

        # http://www.wolframalpha.com/input/?i=curl+%7Bx*y%2Bsin(x)%2B3*x,+x-y-5*x,+cos(2*x)-sin(y)%5E2%7D
        >>> x, y, z = (3.5, 2.1, -3.3)
        >>> (-2 * math.sin(y) * math.cos(y), 2 * math.sin(2 * x), -x - 4)
        (0.8715757724135881, 1.3139731974375781, -7.5)

        # https://www.youtube.com/watch?v=UW4SQz29TDc
        >>> F = lambda x, y, z: (y**4 - x**2 * z**2, x**2 + y**2, -x**2 * y * z)
        >>> curl(F, (1, 3, -2))
        (2.0, -8.0, -106.0)

        >>> F = lambda x, y, z: (8 * exp(-x), cosh(z), - y**2)
        >>> curl(F, (2, -1, 4))
        (-25.289917197127753, 0.0, 0.0)

        # https://www.youtube.com/watch?v=S2rT2zK2bdo
        >>> x, y, z = (2, -1, 4)
        >>> (-(x * y + math.sinh(z)), 0.0, 0.0)
        (-25.289917197127753, 0.0, 0.0)

    '''
    x, y, z = point
    _, Fyx, Fzx = map(d, F(Var(x), y, z))
    Fxy, _, Fzy = map(d, F(x, Var(y), z))
    Fxz, Fyz, _ = map(d, F(x, y, Var(z)))
    return (Fzy - Fyz, Fxz - Fzx, Fyx - Fxy)


if __name__ == '__main__':

    # River flow example: https://www.youtube.com/watch?v=vvzTEbp9lrc
    W = 20     # width of river in meters
    C = 0.1    # max flow divided by (W/2)**2
    F = lambda x, y=0, z=0:  (0.0, C * x * (W - x), 0.0)
    for x in range(W+1):
        print('%d --> %r' % (x, curl(F, (x, 0.0, 0.0))))

    def numeric_derivative(func, x, eps=0.001):
        'Estimate the derivative using numerical methods'
        y0 = func(x - eps)
        y1 = func(x + eps)
        return (y1 - y0) / (2.0 * eps)

    def test(x_array, *testcases):
        for f in testcases:
            print(f.__name__.center(40))
            print('-' * 40)
            for x in map(Var, x_array):
                y = f(x)
                actual = d(y)
                expected = numeric_derivative(f, x, 2**-16)
                print('%7.3f  %12.4f  %12.4f' % (x, actual, expected))
                assert math.isclose(expected, actual, rel_tol=1e-5)
            print('')

    def test_pow_const_base(x):
        return 3.1 ** (2.3 * x + 0.4)

    def test_pow_const_exp(x):
        return (2.3 * x + 0.4) ** (-1.3)

    def test_pow_general(x):
        return (x / 3.5) ** sin(3.5 * x)

    def test_hyperbolics(x):
        return 3 * cosh(1/x) + 5 * sinh(x/2.5) ** 2 - 0.7 * tanh(1.7/x) ** 1.5

    def test_sqrt(x):
        return cos(sqrt(abs(sin(x) + 5)))

    def test_conversions(x):
        return degrees(x ** 1.5 + 18) * radians(0.83 ** x + 37)

    def test_hypot(x):
        return hypot(sin(x), cos(1.1 / x))

    def test_erf(x):
        return (sin(x) * erf(x**0.85 - 3.123) +
                cos(x) * erfc(x**0.851 - 3.25))

    def test_rounders(x):
        return (tan(x) * floor(cos(x**2 + 0.37) * 2.7) +
                log(x) * ceil(cos(x**3 + 0.31) * 12.1) * 10.1 +
                exp(x) * trunc(sin(x**1.4 + 8.0)) * 1234.567)

    def test_inv_trig(x):
        return (atan((x - 0.303) ** 2.9 + 0.1234) +
                acos((x - 4.1) / 3.113) * 5 +
                asin((x - 4.3) / 3.717))

    def test_mod(x):
        return 137.1327 % (sin(x + 0.3) * 40.123) + cos(x) % 5.753

    def test_logs(x):
        return log2(fabs(sin(x))) + log10(fabs(cos(x))) + log1p(fabs(tan(x)))

    def test_fsum(x):
        import random
        random.seed(8675309)
        data = [Num(random.random()**x, random.random()**x) for i in range(100)]
        return fsum(data)

    def test_inv_hyperbolics(x):
        return (acosh(x**1.1234567 + 0.89) + 3.51 * asinh(x**1.234567 + 8.9) +
                atanh(x / 15.0823))

    def test_copysign(x):
        return (copysign(7.17 * x + 5.11, 1.0) + copysign(4.1 * x, 0.0) +
                copysign(8.909 * x + 0.18, -0.0) + copysign(4.321 * x + .12, -1.0) +
                copysign(-3.53 * x + 11.5, 1.0) + copysign(-1.4 * x + 2.1, 0.0) +
                copysign(-9.089 * x + 0.813, -0.0) + copysign(-1.2347 * x, -1.0) +
                copysign(sin(x), x - math.pi))

    def test_combined(x):
        return (1.7 - 3 * cos(x) ** 2 / sin(3 * x) * 0.1 * exp(+cos(x)) +
                sqrt(abs(x - 4.13)) + tan(2.5 * x) * log(3.1 * x**1.5) +
                (4.7 * x + 3.1) ** cos(0.43 * x + 8.1) - 2.9 + tan(-x) +
                sqrt(radians(log(x) + 1.7)) + e / x + expm1(x / pi))

    x_array = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5]
    tests =   [test_combined, test_pow_const_base, test_pow_const_exp,
               test_pow_general, test_hyperbolics, test_sqrt, test_copysign,
               test_inv_trig, test_conversions, test_hypot, test_rounders,
               test_inv_hyperbolics, test_mod, test_logs, test_fsum, test_erf]
    test(x_array, *tests)

    # Run doctests when the underlying C math library matches the one used to
    # generate the code examples (the approximation algorithms vary slightly).
    if 2 + math.sinh(4) == 29.289917197127753:
        import doctest
        print(doctest.testmod())
