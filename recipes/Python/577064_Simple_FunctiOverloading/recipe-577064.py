#!/usr/bin/env python

from functools import wraps

def overloaded(func):
    @wraps(func)
    def overloaded_func(*args, **kwargs):
        for f in overloaded_func.overloads:
            try:
                return f(*args, **kwargs)
            except TypeError:
                pass
        else:
            # it will be nice if the error message prints a list of 
            # possible signatures here
            raise TypeError("No compatible signatures")
    
    def overload_with(func):
        overloaded_func.overloads.append(func)
        return overloaded_func
    
    overloaded_func.overloads = [func]
    overloaded_func.overload_with = overload_with
    return overloaded_func


#############

@overloaded
def foo():
    print 'foo() without args'
    pass

@foo.overload_with
def _(n):
    # note that, like property(), the function's name in 
    # the "def _(n):" line can be arbitrary, the important
    # name is in the "@overloads(a)" line
    print 'foo() with one argument'
    pass

foo()
foo(4)
foo(4, 5) # ERROR: no matching signature
