from sets import Set
import operator
import inspect

class Superposition(Set):
    def __init__(self,*argl):
        super(Superposition,self).__init__(self)
        for arg in argl:
            if isinstance(arg,Set):
                self |= arg
            elif isinstance(arg,list) or isinstance(arg,tuple):
                self |= Set(arg)
            else:
                self.add(arg)

    def eigenstates(self):
        return list(self)

    def _cartesian(self,other,op,order=True):
        if order:
            if isinstance(other,Superposition):
                s = self.__class__([op(x,y) for x in self for y in other])
            else:
                s = self.__class__([op(x,other) for x in self])
        else:
            if isinstance(other,Superposition):
                s = self.__class__([op(y,x) for x in self for y in other])
            else:
                s = self.__class__([op(other,x) for x in self])

        return s
    def __add__(self,other):
        return self._cartesian(other,operator.add)

    __radd__ = __add__

    def __sub__(self,other):
        return self._cartesian(other,operator.sub)

    def __rsub__(self,other):
        return self._cartesian(other,operator.sub,False)

    def __mod__(self,other):
        return self._cartesian(other,operator.mod)

    def __rmod__(self,other):
        return self._cartesian(other,operator.mod,False)

    def __mul__(self,other):
        return self._cartesian(other,operator.mul)

    __rmul__ = __mul__

    def __div__(self,other):
        return self._cartesian(other,operator.div)

    def __rdiv__(self,other):
        return self._cartesian(other,operator.div,False)

    def _comp(self,other,op):
        return self.__class__([x for x in self if op(x,other)])

    def __eq__(self,other):
        return self._comp(other,operator.eq)

    def __lt__(self,other):
        return self._comp(other,operator.lt)

    def __le__(self,other):
        return self._comp(other,operator.le)

    def __gt__(self,other):
        return self._comp(other,operator.gt)

    def __ge__(self,other):
        return self._comp(other,operator.ge)

    def __ne__(self,other):
        if isinstance(other,Superposition):
            return self.__class__([x for x in self if x not in other])
        else:
            return self._comp(other,operator.ne)
    
class Any(Superposition):pass


class All(Superposition):
    def _comp(self,other,op):
        r = super(All,self)._comp(other,op)
        if len(r) == len(self):
            return r
        else:
            return All()

    def __eq__(self,other):
        if isinstance(other,Set):
            r = Set(self) & other
            if len(r) == len(self):
                return All(r)
            else:
                return All()
        elif len(self) == 1 and self.eigenstates()[0] == other:
            print 'in elif'
            return All(self)
        else:
            return All()
    
if __name__ == '__main__':
    a = Superposition(1,2,3)
    b = Superposition(2,3,4)
    print 'a =',a
    print 'b =',b
    print 'a+b',a+b
    print 'a-b',a-b
    print 'b-a',b-a
    print 'a*b',a*b
    print 'a/b',a/b
    print 'b/a',b/a
    print 'a == 1',a==1
    print 'a == 2',a==2
    print 'a == b',a==b
    print 'a != b',a!=b
    print 'b != a',b!=a
    print 'a < 2',a<2
    print 'a > 2',a>2
    print 'a <= 2',a<=2
    print 'a >= 2',a>=2
    print 'a < b',a<b
    print 'a > b',a>b
    print
    a = All(1,2,3)
    b = All(2,3,4)
    print '== All =='
    print
    print 'a == 1',a==1
    print 'a == 2',a==2
    print 'a == b',a==b
    print 'a == a',a==a
    print 'a != b',a!=b
    print 'b != a',b!=a
    print 'a < 2',a<2
    print 'a < 4',a<4
    print 'a > 2',a>2
    print 'a > 0',a>0
    print 'a <= 3',a<=3
    print 'a >= 2',a>=2
    print 'a < b',a<b
    print 'a > b',a>b
    print 'a > a',a>a
    print 'a >= a',a>=a
    print 'All(7,8,9) <= Any(5,6,7)', All(7,8,9) <= Any(5,6,7)
    print 'All(5,6,7) <= Any(7,8,9)', All(5,6,7) <= Any(7,8,9)
    print 'Any(6,7,8) <= All(7,8,9)', Any(6,7,8) <= All(7,8,9)
    print 'MIN: Any(6,7,8) <= All(6,7,8)', Any(6,7,8) <= All(6,7,8)
    print 'MAX: Any(6,7,8) >= All(6,7,8)', Any(6,7,8) >= All(6,7,8)
    import math
    print 'PRIMES range(4,20)', [x for x in range(4,20) if x % All([i for i in xrange(2,int(math.sqrt(x))+1)]) != 0]

    def isprimenumber(num):
        return bool(num % All([i for i in xrange(2,int(math.sqrt(num))+1)]) != 0)

    def isprime(num):
        if isinstance(num,Superposition):
            return bool([x for x in num.eigenstates() if isprimenumber(x) ])
        else:
            return isprimenumber(num)

    def hastwin(num):
        return isprime(num) and isprime(num+Any(+2,-2))


    print 'isprime(7)',isprime(7)
    print 'isprime(10)',isprime(10)
    print 'hastwin(7)',hastwin(7)
    print 'hastwin(23)',hastwin(23)
    
    print '== Strings =='
    a = Any('a','b','c')
    print "a = Any('a','b','c')"
    print "a + '_test'",a + '_test'
