def parameters(only=None, exclude=None, ignore='self'):
    """Returns a dictionary of the calling functions 
       parameter names and values.

       The optional arguments can be used to filter the result:

           only           use this to only return parameters 
                          from this list of names.

           exclude        use this to return every parameter 
                          *except* those included in this list
                          of names.

           ignore         use this inside methods to ignore 
                          the calling object's name. For 
                          convenience, it ignores 'self' 
                          by default.

    """
    import inspect
    args, varargs, varkw, defaults = \
        inspect.getargvalues(inspect.stack()[1][0])
    if only is None:
        only = args[:]
        if varkw:
            only.extend(defaults[varkw].keys())
            defaults.update(defaults[varkw])
    if exclude is None:
        exclude = []
    exclude.append(ignore)
    return dict([(attrname, defaults[attrname])
        for attrname in only if attrname not in exclude])
