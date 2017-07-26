class RestrictedDict(dict):
    """
    Stores the properties of an object. It's a dictionary that's
    restricted to a tuple of allowed keys. Any attempt to set an invalid
    key raises an error.
    
    >>> p = RestrictedDict(('x','y'))
    >>> print p
    RestrictedDict(('x', 'y'), {})
    >>> p['x'] = 1
    >>> p['y'] = 'item'
    >>> print p
    RestrictedDict(('x', 'y'), {'y': 'item', 'x': 1})
    >>> p.update({'x': 2, 'y': 5})
    >>> print p
    RestrictedDict(('x', 'y'), {'y': 5, 'x': 2})
    >>> p['x']
    2
    >>> p['z'] = 0
    Traceback (most recent call last):
    ...
    KeyError: 'z is not allowed as key'
    >>> q = RestrictedDict(('x', 'y'), x=2, y=5)
    >>> p==q
    True
    >>> q = RestrictedDict(('x', 'y', 'z'), x=2, y=5)
    >>> p==q
    False
    >>> len(q)
    2
    >>> q.keys()
    ['y', 'x']
    >>> q._allowed_keys
    ('x', 'y', 'z')
    >>> p._allowed_keys = ('x', 'y', 'z')
    >>> p['z'] = 3
    >>> print p
    RestrictedDict(('x', 'y', 'z'), {'y': 5, 'x': 2, 'z': 3})

    """
    
    def __init__(self, allowed_keys, seq=(), **kwargs):
        """
        Initializes the class instance. The allowed_keys tuple is
        required, and it cannot be changed later.
        If seq and/or kwargs are provided, the values are added (just
        like a normal dictionary).
        """
        super(RestrictedDict, self).__init__()
        self._allowed_keys = tuple(allowed_keys)
        # normalize arguments to a (key, value) iterable
        if hasattr(seq, 'keys'):
            get = seq.__getitem__
            seq = ((k, get(k)) for k in seq.keys())
        if kwargs:
            from itertools import chain
            seq = chain(seq, kwargs.iteritems())
        # scan the items keeping track of the keys' order
        for k, v in seq:
            self.__setitem__(k, v)

    def __setitem__(self, key, value):
        """Checks if the key is allowed before setting the value"""
        if key in self._allowed_keys:
            super(RestrictedDict, self).__setitem__(key, value)
        else:
            raise KeyError("%s is not allowed as key" % key)

    def update(self, e=None, **kwargs):
        """
        Equivalent to dict.update(), but it was needed to call
        RestrictedDict.__setitem__() instead of dict.__setitem__
        """
        try:
            for k in e:
                self.__setitem__(k, e[k])
        except AttributeError:
            for (k, v) in e:
                self.__setitem__(k, v)
        for k in kwargs:
            self.__setitem__(k, kwargs[k])

    def __eq__(self, other):
        """
        Two RestrictedDicts are equal when their dictionaries and allowed keys
        are all equal.
        """
        if other is None:
            return False
        try:
            allowedcmp = (self._allowed_keys == other._allowed_keys)
            if allowedcmp:
                dictcmp = super(RestrictedDict, self).__eq__(other)
            else:
                return False
        except AttributeError:
            #Other is not a RestrictedDict
            return False
        return bool(dictcmp)

    def __ne__(self, other):
        """x.__ne__(y) <==> not x.__eq__(y)"""
        return not self.__eq__(other)

    def __repr__(self):
        """Representation of the RestrictedDict"""
        return 'RestrictedDict(%s, %s)' % (self._allowed_keys.__repr__(),
                                     super(RestrictedDict, self).__repr__())
if __name__ == '__main__':
    import doctest
    doctest.testmod()
