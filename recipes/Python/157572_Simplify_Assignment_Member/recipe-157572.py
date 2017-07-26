import inspect

def AssignMemberVariablesFromParameters(exclude=None, onlyInclude=None):
    """Assign member variables in the caller's object from the caller's parameters.

    The caller should be a method associated with an object. Keyword arguments
    are supported, but variable arguments are not since they don't have names.
    exclude is an optional iterable that specifies names to be explicitly
    excluded. If the optional iterable onlyInclude is specified,
    parameters / member variables not in onlyInclude will be ignored.

    >>> class c:
    ...     def __init__(self, a, b, c=3, **kwargs):
    ...        AssignMemberVariablesFromParameters()
    ...
    ...     def ignore_a_b(self, a, b, c, d):
    ...        AssignMemberVariablesFromParameters(exclude=['a', 'b'])
    ...
    ...     def ignore_c_d(alternateNameForSelf, a, b, c, d):
    ...        AssignMemberVariablesFromParameters(onlyInclude=['a', 'b'])

    >>> x = c(1, 2, d=4)
    >>> (x.a, x.b, x.c, x.d)
    (1, 2, 3, 4)

    >>> x.ignore_a_b(10, 20, 30, 40)
    >>> (x.a, x.b, x.c, x.d)
    (1, 2, 30, 40)

    >>> x.ignore_c_d(100, 200, 300, 400)
    >>> (x.a, x.b, x.c, x.d)
    (100, 200, 30, 40)

    >>> class c:
    ...     __slots__ = ['a', 'b', 'c']
    ...
    ...     def __init__(self, a, b):
    ...        AssignMemberVariablesFromParameters()

    >>> x = c(1, 2)
    >>> (x.a, x.b)
    (1, 2)
    """

    args, varargs, varkw, defaults = inspect.getargvalues(inspect.stack()[1][0])

    self = args[0]

    if exclude == None:
        exclude = []
    else:
        exclude = [arg for arg in exclude]

    if onlyInclude == None:
        onlyInclude = [arg for arg in args if arg != self]
        if varkw:
            onlyInclude += [arg for arg in defaults[varkw].keys() if arg != self]

    for arg in onlyInclude:
        if arg not in exclude:
            if arg in defaults:
                value = defaults[arg]
            elif varkw and arg in defaults[varkw]:
                value = defaults[varkw][arg]
            else:
                value = None
            exec 'defaults[self].%s = %s' % (arg, 'value')
