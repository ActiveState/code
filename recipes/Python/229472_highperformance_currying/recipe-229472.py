# Consider this code in module a.py:
import new
def curry1(func, arg):
    return new.instancemethod(func, arg, object)
def curry2(func, arg):
    def curried(*args): return func(args, *args)
    return curried
def f(a, b, c): return a, b, c
g1=curry1(f, 23)
g2=curry2(f, 23)
# g1 and g2 have the same behavior.  But NOT the same performance...:
#[alex@lancelot ba]$ timeit.py -c -s'import a' 'a.g1(45,67)'
# 1000000 loops, best of 3: 1.37 usec per loop
#[alex@lancelot ba]$ timeit.py -c -s'import a' 'a.g2(45,67)'
# 100000 loops, best of 3: 2.4 usec per loop
# curry1-produced g1 is faster enough than curry2-produced g2 to make
# this worth keeping in mind for curried functions that must be run
# as part of a program's performance bottleneck.
