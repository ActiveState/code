#!/usr/bin/env python

import functools
import warnings
warnings.simplefilter("once", category=(PendingDeprecationWarning, DeprecationWarning))

def deprecate(msg, klass=PendingDeprecationWarning):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, klass, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    @deprecate("This function will be deprecated in the future. Use new_function().")
    def old_function(a, b):
        new_function(a, b, 0)

    def new_function(a, b, c):
        print(a+b+c)

    old_function(1, 2)
