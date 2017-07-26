# Remove duplicates from a list:
>>> L = [1,2,2,3,3,3]
>>> [x for x in L if x not in locals()['_[1]'].__self__]
[1,2,3]


# That's a bit ugly, so let's encapsulate it in a function.
# Be carefull with nested list comprehensions. The inner one is
# called "_[2]" (or "_[3]", and so on if you nest them deeply).
def thislist():
    """Return a reference to the list object being constructed by the
    list comprehension from which this function is called. Raises an
    exception if called from anywhere else.
    """
    import sys
    d = sys._getframe(1).f_locals
    nestlevel = 1
    while '_[%d]' % nestlevel in d:
        nestlevel += 1
    return d['_[%d]' % (nestlevel - 1)].__self__

# More readable now:
>>> L = [1,2,2,3,3,3]
>>> [x for x in L if x not in thislist()]
[1,2,3]


# At any given point in the construction, the list is a fully functional
# list object. You can even call mutating methods on it.
# For example:

# Remove duplicates from a list, retaining only the *last* item from 
# each equivalency class:
>>> L = ['ab','a'+'b']
>>> map(id, L)
[16333632, 16332416]
>>> L2 = [x for x in L if x not in thislist() \
                        or not thislist().remove(x)]
>>> L2
['ab']
>>> map(id, L2) # make sure it worked...
[16332416]


# Another example: Finding prime numbers (Python 2.3+)
import itertools, sys, math

def primes_less_than(N):
    return [p for p in itertools.chain([2],xrange(3,N,2))
            if 0 not in itertools.imap(lambda x:p%x,
                                       itertools.takewhile(
                                           lambda v:v <= math.sqrt(p),
                                           thislist() ))]

def first_N_primes(N):
    return [p for p in itertools.takewhile(lambda _,L=thislist():len(L) < N,
                                           itertools.chain([2],xrange(3,sys.maxint,2)))
            if 0 not in itertools.imap(lambda x:p%x,
                                       itertools.takewhile(
                                           lambda v:v <= math.sqrt(p),
                                           thislist()))]

# For lazy typists:
plt = primes_less_than
fnp = first_N_primes

>>> plt(20)
[2, 3, 5, 7, 11, 13, 17, 19]
>>> fnp(10)
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
