def flatten(x):
    r"""
    
    >>> flatten("hello")
    'hello'
    >>> flatten({"a":[["hi"]]})
    {'a': [['hi']]}
    >>> flatten(None) is None
    True
    >>> flatten(3)
    3
    >>> flatten([0, [1, ["two"]]])
    [0, 1, 'two']
    >>> flatten( (0, (1, ("two",))) )
    (0, 1, 'two')
    >>> flatten([0, [1, 2], 3, ([4, 5], 6)])
    [0, 1, 2, 3, 4, 5, 6]
    >>> flatten( (0, 1, (i + 1 for i in xrange(1, 3)) ) )
    (0, 1, 2, 3)
    >>> flatten([[[[[0]]]]])
    [0]
    >>> flatten([0, [[{"a":[["hi"]]}]]])
    [0, {'a': [['hi']]}]
    
    """
    
    if isinstance(x, basestring):
        return x
    if hasattr(x, "__iter__"):
        if hasattr(x, "items"):
            return x
    else:
        return x
    
    is_tuple = isinstance(x, tuple)
    
    # leave exception here unhandled
    # if conversion to list fails
    x = list(x)
    x.reverse()
    
    r = []
    while x:
        y = x.pop(-1)
        if isinstance(y, basestring):
            r.append(y)
            continue
        if hasattr(y, "__iter__"):
            if hasattr(y, "items"):
                r.append(y)
                continue
        else:
            r.append(y)
            continue
        # leave exception here unhandled
        # if conversion to list fails
        y = list(y)
        y.reverse()
        x.extend(y)
        
    if is_tuple:
        return tuple(r)
    else:
        return r
