_NOTFOUND = object()


class Flipdict(dict):
    """An injective (one-to-one) python dict.  Ensures that each key maps
    to a unique value, and each value maps back to that same key.

    A Flipdict is a dict, implementing the dict API::
        >>> fd = Flipdict({1: 'one', 2: 'two', 3: 'three'})
        >>> fd[1]
        'one'
        >>> fd.setdefault(4, 'four')
        'four'
        >>> fd
        Flipdict({1: 'one', 2: 'two', 3: 'three', 4: 'four'})

    Each Flipdict has a "flip" attribute, its inverse mapping::
        >>> fd is fd.flip.flip
        True
        >>> sorted(fd.flip.items())
        [('four', 4), ('one', 1), ('three', 3), ('two', 2)]

    Just like a dict, remapping a key will erase the old mapping.
    IMPORTANT: Suppose a Flipdict maps key K to value V. Then mapping a
    *new* key to the value V will raise KeyError::
        >>> fd[4444] = 'four'
        Traceback (most recent call last):
        ....
        KeyError: "(key,val) would erase mapping for value 'four'"

    This avoids a subtle situation.  The alternative is to silently erase
    the existing pair (K,V)!  Instead, explicitly use the "flip" attribute
    like a python dict::
        >>> fd.flip['four'] = 4444
        >>> fd
        Flipdict({1: 'one', 2: 'two', 3: 'three', 4444: 'four'})
    """

    def __init__(self, *args, **kw):
        """Cf. dict.__init__

        Examples::
            >>> fd = Flipdict( zip((1, 2, 3), ('one', 'two', 'three')) )
            >>> fd == Flipdict({1: 'one', 2: 'two', 3: 'three'})
            True
            >>> fd == Flipdict(one=1, two=2, three=3).flip
            True

        IMPORTANT: Mapping many keys to the same value will raise KeyError.
        """
        self._flip = dict.__new__(self.__class__)
        setattr(self._flip, "_flip", self)
        for key, val in dict(*args, **kw).iteritems():
            self[key] = val

    @property
    def flip(self):
        """The inverse mapping.

        Examples::
            >>> fd = Flipdict({1: 'one', 2: 'two', 3: 'three'})
            >>> fd.flip['two']
            2
            >>> fd is fd.flip.flip
            True
        """
        return self._flip


    #{ Non-mutating methods that are NOT delegated to the dict superclass.

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, dict(self))

    __str__ = __repr__

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, keys, value=None):
        """
        NOTE: This method is mostly useless for a Flipdict, because
        each key must map to a UNIQUE value.
        """
        return cls(dict.fromkeys(keys, value))

    #}


    #{ Mutating methods.  These must keep the inverse mapping in sync!

    def __setitem__(self, key, val):
        """self[key] = val (and self.flip[val] = key)

        Remapping a key will erase the old mapping (just like a dict)::
            >>> fd = Flipdict(one=1, two=2)
            >>> fd['two'] = 22
            >>> fd
            Flipdict({'two': 22, 'one': 1})
            >>> fd.flip
            Flipdict({1: 'one', 22: 'two'})

        Just like a dict, remapping a key will erase the old mapping.
        IMPORTANT: Suppose a Flipdict maps key K to value V. Then mapping a
        *new* key to the value V will raise KeyError::
            >>> fd['twenty-two'] = 22
            Traceback (most recent call last):
            ....
            KeyError: '(key,val) would erase mapping for value 22'

        This avoids a subtle situation.  The alternative is to silently
        erase the existing pair (K,V)!  Instead, explicitly use the "flip"
        attribute like a python dict::
            >>> fd.flip[22] = 'twenty-two'
            >>> sorted(fd.items())
            [('one', 1), ('twenty-two', 22)]
        """
        k = self._flip.get(val, _NOTFOUND)
        if not (k is _NOTFOUND or k==key):
            raise KeyError('(key,val) would erase mapping for value %r' % val)

        v = self.get(key, _NOTFOUND)
        if v is not _NOTFOUND:
            dict.__delitem__(self._flip, v)

        dict.__setitem__(self,       key, val)
        dict.__setitem__(self._flip, val, key)

    def setdefault(self, key, default = None):
        # Copied from python's UserDict.DictMixin code.
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def update(self, other = None, **kwargs):
        # Copied from python's UserDict.DictMixin code.
        # Make progressively weaker assumptions about "other"
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):  # iteritems saves memory and lookups
            for k, v in other.iteritems():
                self[k] = v
        elif hasattr(other, 'keys'):
            for k in other.keys():
                self[k] = other[k]
        else:
            for k, v in other:
                self[k] = v
        if kwargs:
            self.update(kwargs)

    def __delitem__(self, key):
        val = dict.pop(self, key)
        dict.__delitem__(self._flip, val)

    def pop(self, key, *args):
        val = dict.pop(self, key, *args)
        dict.__delitem__(self._flip, val)
        return val

    def popitem(self):
        key, val = dict.popitem(self)
        dict.__delitem__(self._flip, val)
        return key, val

    def clear(self):
        dict.clear(self)
        dict.clear(self._flip)


def makepair(*args, **kw):
    """Returns a pair:  the Flipdict(*args, **kw) and its inverse.

    Example::
        >>> chr2num, num2chr = makepair({'a':1, 'b':2, 'c':3})
        >>> chr2num['z'] = 26
        >>> num2chr.items()
        [(1, 'a'), (2, 'b'), (3, 'c'), (26, 'z')]
    """
    fd = Flipdict(*args, **kw)
    return fd, fd.flip


if __name__=='__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
