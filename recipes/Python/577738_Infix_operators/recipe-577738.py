# definition of an Infix operator class
# this recipe also works in jython
# calling sequence for the infix is either:
#  x |op| y
# or:
# x <<op>> y

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

# Examples

# simple multiplication
x=Infix(lambda x,y: x*y)
print 2 |x| 4
# => 8

# class checking
isa=Infix(lambda x,y: x.__class__==y.__class__)
print [1,2,3] |isa| []
print [1,2,3] <<isa>> []
# => True

# inclusion checking
is_in=Infix(lambda x,y: y.has_key(x))
print 1 |is_in| {1:'one'}
print 1 <<is_in>> {1:'one'}
# => True

# an infix div operator
import operator
div=Infix(operator.div)
print 10 |div| (4 |div| 2)
# => 5

# functional programming (not working in jython, use the "curry" recipe! )
def curry(f,x):
    def curried_function(*args, **kw):
        return f(*((x,)+args),**kw)
    return curried_function
curry=Infix(curry)

add5= operator.add |curry| 5
print add5(6)
# => 11
