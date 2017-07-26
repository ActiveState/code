import inspect

def get_arg_value(func, argname, args, kwargs):
    """

    This function is meant to be used inside decorators, when you want
    to find what value will be available inside a wrapped function for
    a particular argument name.  It handles positional and keyword
    arguments and takes into account default values.  For example:

    >>> def foo(x, y): pass
    ... 
    >>> get_arg_value(foo, 'y', [1, 2], {})
    2
    >>> get_arg_value(foo, 'y', [1], {'y' : 2})
    2
    >>> def foo(x, y, z=300): pass
    ... 
    >>> get_arg_value(foo, 'z', [1], {'y' : 2})
    300
    >>> get_arg_value(foo, 'z', [1], {'y' : 2, 'z' : 5})
    5

    """
    # first check kwargs
    if argname in kwargs:
        return kwargs[argname]
    # OK.  could it be a positional argument?
    regargs, varargs, varkwargs, defaults=inspect.getargspec(func)
    if argname in regargs:
        regdict=dict(zip(regargs, args))
        if argname in regdict:
            return regdict[argname]
    defaultdict=dict(zip(reversed(regargs), defaults))
    if argname in defaultdict:
        return defaultdict[argname]
    raise ValueError("no such argument: %s" % argname)

        
