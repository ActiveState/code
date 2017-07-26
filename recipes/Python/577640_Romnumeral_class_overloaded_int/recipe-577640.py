'''
The int methods of this Roman class are overloaded to return new
Roman instances, so you can use it to perform wrap ints and
perform basic math, like this:

>>> x = Roman(3)
>>> y = Roman(30)

>>> print x, y
Roman(3, III) Roman(30, XXX)

>>> print x + y
Roman(33, XXXIII)

>>> print x * y
Roman(90, LXXXX)

>>> print y / x
Roman(10, X)

>>> print Roman(2) ** 3
Roman(8, VIII)

>>> print Roman(25) % 11 
Roman(3, III)

>>> print Roman(-45)
Roman(-45, -DCCCCLV)

>>> sum(map(Roman, range(10)))
Roman(45)

>>> reduce(operator.mul, map(Roman, range(1, 5)))
Roman(24)

>>> print sum(map(Roman, range(10)))
Roman(45, XXXXV)

>>> print reduce(operator.mul, map(Roman, range(1, 5)))
Roman(24, XXIV)
'''

__author__ = "Thom"
__copyright__ = None
__license__ = "Python"

import re

def returnthisclassfrom(methods):
    '''
    Class decorator by Alex Martelli.

    see ('http://stackoverflow.com/questions/1242589/
          subclassing-int-to-attain-a-hex-representation/1243045#1243045)
    '''
    def wrapit(cls, method):
        return lambda *a: cls(method(*a))
    def dowrap(cls):
        for n in methods:
          method = getattr(cls, n)
          setattr(cls, n, wrapit(cls, method))
        return cls

    return dowrap

methods = "mul add sub div pow mod divmod".split()
methods += [c + s for s in methods for c in list('ir')]
methods = ['__%s__' % s for s in methods]
methods = set(methods) & set(dir(int))

@returnthisclassfrom(methods)
class Roman(int):

    i_ones = range(10)
    r_ones = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    ones_i2r = dict(zip(i_ones, r_ones))
    
    i_mul = [10, 50, 100, 500, 1000]
    r_mul = ["X", "L", "C", "D", "M"]
    mul_i2r = dict(zip(i_mul, r_mul))

    i = i_ones + i_mul
    r = r_ones + r_mul
    rom2int = dict(zip(r, i))
    re_rom = re.compile('|'.join(sorted(r, key=len, reverse=True)))

    def as_roman(self):
        
        sign = "-" if self < 0 else ""
        res = [sign]
        n = int(self)
        mul_i2r = self.mul_i2r
        
        for x in reversed(self.i_mul):
            
            div, mod = divmod(n, x)
            n = mod
            res.append(mul_i2r[x] * div)

        res.append(self.ones_i2r[n])

        return "".join(res)

    def __str__(self):
        return "Roman(%d, %s)" % (self, self.as_roman())

    def __repr__(self):
        return "Roman(%d)" % self

    @classmethod
    def fromstring(cls, s):
        return cls(sum(map(cls.rom2int.get, cls.re_rom.findall(s))))
        
            
if __name__ == "__main__":
    
    for x in range(1, 1001):
        r = Roman(x)
        assert r == Roman.fromstring(r.as_roman())
        print x, r

    print '\n'
    
    import operator
    x, y = Roman(20), Roman(5)
    print 'x =', x
    print 'y = ', y

    for s in "add sub div mul".split():
        print '%s(x, y) = %s' % (s, getattr(operator, s)(x, y))

    print '\n'

    x -= 1
    print 'x % y = ', x % y
            
