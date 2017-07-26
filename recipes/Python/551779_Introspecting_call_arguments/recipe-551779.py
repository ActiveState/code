def getcallargs(func, *args, **kwds):
    '''Get the actual value bounded to each formal parameter when calling
    `func(*args,**kwds)`.

    It works for methods too (bounded, unbounded, staticmethods, classmethods).

    @returns: `(bindings, missing_args)`, where:
        - `bindings` is a mapping of every formal parameter (including *varargs
           and **kwargs if present) of the function to the respective bounded value.
        - `missing_args` is a tuple of the formal parameters whose value was not
           provided (i.e. using the respective default value)

    Examples::
        >>> def func(a, b='foo', c=None, *x, **y):
        ...     pass
        >>> getcallargs(func, 5)
        ({'a': 5, 'y': {}, 'c': None, 'b': 'foo', 'x': ()}, ('b', 'c'))
        >>> getcallargs(func, 5, 'foo')
        ({'a': 5, 'y': {}, 'c': None, 'b': 'foo', 'x': ()}, ('c',))
        >>> getcallargs(func, 5, c=['a', 'b'])
        ({'a': 5, 'y': {}, 'c': ['a', 'b'], 'b': 'foo', 'x': ()}, ('b',))
        >>> getcallargs(func, 5, 6, 7, 8)
        ({'a': 5, 'y': {}, 'c': 7, 'b': 6, 'x': (8,)}, ())
        >>> getcallargs(func, 5, z=3, b=2)
        ({'a': 5, 'y': {'z': 3}, 'c': None, 'b': 2, 'x': ()}, ('c',))
    '''
    arg2value = {}
    f_name = func.func_name
    spec_args, varargs, varkw, defaults = getargspec(func)
    # handle methods
    if ismethod(func):
        # implicit 'self' (or 'cls' for classmethods) argument: func.im_self
        if func.im_self is not None:
            arg2value[spec_args.pop(0)] = func.im_self
        elif not args or not isinstance(args[0], func.im_class):
            got = args and ('%s instance' % type(args[0]).__name__) or 'nothing'
            raise TypeError('unbound method %s() must be called with %s instance '
                            'as first argument (got %s instead)' %
                            (f_name, func.im_class.__name__, got))
    num_args = len(args)
    has_kwds = bool(kwds)
    num_spec_args = len(spec_args)
    num_defaults = len(defaults or ())
    # get the expected arguments passed positionally
    arg2value.update(izip(spec_args,args))
    # get the expected arguments passed by name
    for arg in spec_args:
        if arg in kwds:
            if arg in arg2value:
                raise TypeError("%s() got multiple values for keyword "
                                "argument '%s'" % (f_name,arg))
            else:
                arg2value[arg] = kwds.pop(arg)
    # fill in any missing values with the defaults
    missing = []
    if defaults:
        for arg,val in izip(spec_args[-num_defaults:],defaults):
            if arg not in arg2value:
                arg2value[arg] = val
                missing.append(arg)
    # ensure that all required args have a value
    for arg in spec_args:
        if arg not in arg2value:
            num_required = num_spec_args - num_defaults
            raise TypeError('%s() takes at least %d %s argument%s (%d given)'
                            % (f_name, num_required,
                               has_kwds and 'non-keyword ' or '',
                               num_required>1 and 's' or '', num_args))
    # handle any remaining named arguments
    if varkw:
        arg2value[varkw] = kwds
    elif kwds:
        raise TypeError("%s() got an unexpected keyword argument '%s'" %
                        (f_name, iter(kwds).next()))
    # handle any remaining positional arguments
    if varargs:
        if num_args > num_spec_args:
            arg2value[varargs] = args[-(num_args-num_spec_args):]
        else:
            arg2value[varargs] = ()
    elif num_spec_args < num_args:
        raise TypeError('%s() takes %s %d argument%s (%d given)' %
                        (f_name, defaults and 'at most' or 'exactly',
                         num_spec_args, num_spec_args>1 and 's' or '', num_args))
    return arg2value, tuple(missing)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
