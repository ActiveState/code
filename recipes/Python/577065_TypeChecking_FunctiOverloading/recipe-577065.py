#!/usr/bin/env python

from functools import wraps


def returns(rettype):
    def check(ret):
        if not isinstance(ret, rettype): raise InputParameterError()
        return ret
    def returnchecker(func):
        @wraps(func)
        def _func(*args, **kwargs):
            return check(func(*args, **kwargs))

        _func.returns = rettype
        return _func
    return returnchecker

def takes(*argtypes, **kwtypes):
    def check(args, kwargs):
        if not len(args) == len(argtypes): raise InputParameterError()
        if not all(isinstance(a, b) for a, b in zip(args, argtypes)): raise InputParameterError()

        if not len(kwargs) == len(kwtypes): raise InputParameterError()
        if not set(kwargs) == set(kwtypes) : raise InputParameterError()
        if not all(isinstance(kwargs[kw], kwtypes[kw]) for kw in kwtypes): raise InputParameterError()

    def typechecker(func):
        @wraps(func)
        def _func(*args, **kwargs):
            check(args, kwargs)
            return func(*args, **kwargs)

        _func.signature = argtypes, kwtypes
        return _func
    return typechecker

## note: there is a more comprehensive signature checking recipe #426123
## http://code.activestate.com/recipes/426123-method-signature-checking-decorators/
## this recipe is compatible with that recipe, simply copy that recipe to 
## "signature.py" and uncomment the following import lines ##
##
## from signature import *

class InputParameterError(Exception): pass
def overloaded(func):
    @wraps(func)
    def overloaded_func(*args, **kwargs):
        for f in overloaded_func.overloads:
            try:
                return f(*args, **kwargs)
            except (InputParameterError, TypeError):
                pass
        else:
            raise TypeError("No compatible signatures")

    def overload_with(func):
        overloaded_func.overloads.append(func)
        return overloaded_func
    overloaded_func.overloads = [func]
    overloaded_func.overload_with = overload_with
    return overloaded_func

#############


if __name__ == '__main__':
    @overloaded
    def a():
        print 'no args a'
        pass
    @a.overload_with
    def a(n):
        print 'arged a'
        pass

    a()
    a(4)

    @overloaded
    @returns(int)
    @takes(int, int, float)
    def foo(a, b, c):
        return int(a * b * c)

    @foo.overload_with
    @returns(int)
    @takes(int, float, int, int)
    def foo(a, b, c, d):
        return int(a + b + c)

    @foo.overload_with
    @returns(int)
    @takes(int, float, c=int)
    def foo(a, b, c):
        return int(a + b + c)

    print foo(2, 3, 4.)
    print foo(10, 3., c=30)
    print foo(1, 9., 3, 3)
    print foo('string')
