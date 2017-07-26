def bindfunction(f):
    def bound_f(*args, **kwargs):
        return f(bound_f, *args, **kwargs)
    bound_f.__name__ = f.__name__
    return bound_f

# ----- Examples of use ----------

>>> @bindfunction
... def factorial(this_function, n):
...     if n > 0:
...         return n * this_function(n - 1)
...     else:
...         return 1
... 
>>> factorial(5)
120
>>> fac = factorial
>>> factorial = 'spam'
>>> fac(8) # still works!
40320

>>> @bindfunction
... def counter(counter, total=None):
...     if total is not None:
...             counter.total = total
...     else:
...             counter.total += 1
...             return counter.total
... 
>>> counter(0)
>>> counter()
1
>>> counter()
2
>>> c = counter
>>> counter = 'Ni'
>>> c()
3
>>> c()
4
