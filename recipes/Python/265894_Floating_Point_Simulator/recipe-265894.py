prec = 8     # number of decimal digits (must be under 15)

class F:
    def __init__(self, value, full=None):
        self.value = float('%.*e' % (prec-1, value))
        if full is None:
            full = self.value
        self.full = full
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return "F(%s, %r)" % (self, self.full)
    def error(self):
        ulp = float('1'+('%.4e' % self.value)[-5:]) * 10 ** (1-prec)
        return int(abs(self.value - self.full) / ulp)
    def __coerce__(self, other):
        if not isinstance(other, F):
            return (self, F(other))
        return (self, other)
    def __add__(self, other):
        return F(self.value + other.value, self.full + other.full)
    def __sub__(self, other):
        return F(self.value - other.value, self.full - other.full)
    def __mul__(self, other):
        return F(self.value * other.value, self.full * other.full)
    def __div__(self, other):
        return F(self.value / other.value, self.full / other.full)
    def __neg__(self):
        return F(-self.value, -self.full)
    def __abs__(self):
        return F(abs(self.value), abs(self.full))
    def __pow__(self, other):
        return F(pow(self.value, other.value), pow(self.full, other.full))
    def __cmp__(self, other):
        return cmp(self.value, other.value)

# Example:  Show failure of the associative law (Knuth Vol. 2 p.214)
u, v, w = F(11111113), F(-11111111), F(7.51111111)
assert (u+v)+w == 9.5111111
assert u+(v+w) == 10

# Example:  Show failure of the commutative law for addition
assert u+v+w != v+w+u

# Example:  Show failure of the distributive law (Knuth Vol. 2 p.215)
u, v, w = F(20000), F(-6), F(6.0000003)
assert u*v == -120000
assert u*w == 120000.01
assert v+w == .0000003
assert (u*v) + (u*w) == .01
assert u * (v+w) == .006

# Example:  Compare numerical accuracy of three appoaches to computing averages

def avgsum(data):       # Sum all of the elements
    return sum(data, F(0)) / len(data)

def avgrun(data):       # Make small adjustments to a running mean
    m = data[0]
    k = 1
    for x in data[1:]:
        k += 1
        m += (x-m)/k    # Recurrence formula for mean
    return m

def avgrun_kahan(data): # Adjustment method with Kahan error correction term
    m = data[0]
    k = 1
    dm = 0
    for x in data[1:]:
        k += 1
        adjm = (x-m)/k - dm
        newm = m + adjm
        dm = (newm - m) - adjm
        m = newm
    return m

import random
prec = 5
data = [F(random.random()*10-5) for i in xrange(1000)]
print '%s\t%s\t%s' %('Computed', 'ULP Error', 'Method')
print '%s\t%s\t%s' %('--------', '---------', '------')
for f in avgsum, avgrun, avgrun_kahan:
    result = f(data)
    print '%s\t%6d\t\t%s' % (result, result.error(), f.__name__)
print '\n%r\tbaseline average using full precision' % result.full

# Sample output from the above example
#
# Computed	ULP Error	Method
# --------	---------	------
# -0.020086	    15		avgsum
# -0.020061	     9		avgrun
# -0.020072	     1		avgrun_kahan
# 
# -0.020070327734999997	baseline average using full precision
