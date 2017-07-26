def namespace():
    '''Create an empty module to be used as generic namespace.

    >>> ns = namespace()
    >>> dir(ns)
    []

    >>> ns.member = 'value'
    >>> ns.member
    'value'
    '''

    import imp
    ns = imp.new_module('')
    for attr in dir(ns):
        delattr(ns, attr)
    return ns
