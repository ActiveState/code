# Simple series generator with
# generators & decorators.
# Author : Anand B Pillai

# Beginning of recipe

def myfunc(**kwds):

    def func(f):
        # Condition function
        cond = kwds['condition']
        # Processing function
        proc = kwds['process']
        # Number of items
        num = kwds['number']

        x, l = 0, []
        for item in f():
            
            if cond and cond(item):
                if proc: item=proc(item)
                l.append(item)
                x += 1
                
            if x==num:
                break

        return l

    return func

def series(condition=None, process=None, number=10):
    """ Infinite integer generator """

    @myfunc(condition=condition,process=process,number=number)    
    def wrapper():
        x = 1
        while 1:
            yield x
            x += 1

    return wrapper

# End of recipe
-----snip-------------snip-------------------------
Examples.
  
def prime(x):
    is_prime=True
    for y in range(2,int(pow(x,0.5)) + 1):
        if x % y==0:
            is_prime=False
            break

    return is_prime

# Print first 10 prime numbers
print series(condition=prime, process=None, number=10)
[1, 2, 3, 5, 7, 11, 13, 17, 19, 23]
# Print first 10 odd numbers
print series(condition=lambda x: x%2, process=None, number=10)
[1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
# Print squares of first 10 numbers
print series(condition=lambda x: x, process=lambda x:  x*x, number=10)
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# Print a few random numbers
import random
print series(condition=lambda x: x, process=lambda x: random.random(), number=10)
