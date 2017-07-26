# Numerical Integration using Method of Exhaustion
# http://en.wikipedia.org/wiki/Method_of_exhaustion
# FB - 201012212
import math

def integ(fun, a, b, maxIt):
    ba = b - a
    s = 0.0
    n2 = 1
    for n in range(1, maxIt):
        sgn = 1
        n2 *= 2
        for m in range(1, n2):
            s += (sgn * fun(a + m * ba / n2) / n2)
            sgn = -sgn
    return s * ba

print integ(lambda x: math.sqrt(4.0 - x * x), 0.0, 2.0, 20)
