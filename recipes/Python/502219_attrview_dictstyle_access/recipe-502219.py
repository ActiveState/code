class attrview(object):
    """Wrapper class that provides a dictionary-style, dynamic access to
    the properties of the wrapped object.  Any mutating map operations
    done to the wrapper mutate the wrapped object.

    Because objects may implement attributes using __getattr__ and
    friends, and there is no __dir__ method for objects to specify
    these attributes, it is not possible to enumerate the attributes
    of an object in general.  attrview does not implement the parts of
    the dictionary interface that assume the set of keys is
    deterministic.  Notably, __iter__, keys, values, and items are
    unimplemented.

    """
    def __init__(self, obj):
        """Return an attrview wrapper which provides dictionary-style, dynamic
        access to the properties of the wrapped object.

        """
        self.__wrapped = obj

    def __contains__(self, prop):
        """Return true if the wrapped object has property prop, else False.

        """
        return hasattr(self.__wrapped, prop)

    def __delitem__(self, prop):
        """Delete the property prop from the wrapped object."""
        if not hasattr(self.__wrapped, prop):
            raise KeyError(prop)
        delattr(self.__wrapped, prop)

    def __getitem__(self, prop):
        """Return the value of property prop on the wrapped object."""
        if not hasattr(self.__wrapped, prop):
            raise KeyError(prop)
        return getattr(self.__wrapped, prop)

    def __setitem__(self, prop, val):
        """Set the value of property prop on the wrapped object to val."""
        setattr(self.__wrapped, prop, val)

    def get(self, prop, default=None):
        """Return the value of property prop on the wrapped object if present,
        else default.

        """
        return getattr(self.__wrapped, prop, default)

    def has_key(self, prop):
        """Return true if the wrapped object has property prop, else False.

        """
        return hasattr(self.__wrapped, prop)

    def setdefault(self, prop, val=None):
        """Return self.get(prop, val).  Also set the property prop on the
        wrapped object to val if it currently does not exist.

        """
        if hasattr(self.__wrapped, prop):
            return getattr(self.__wrapped, prop)
        else:
            setattr(self.__wrapped, prop, val)
            return val

    def update(self, d, **kw):
        """Update the properties of the wrapped object from d and kw, with the
        same semantics as dict.update.

        if d has keys, for k in d: self[k] = d[k]
        else, for k, v in d: self[k] = v
        then, for k in kw: self[k] = kw[k].

        """
        if hasattr(d, 'keys'):
            for k in d:
                self[k] = d[k]
        else:
            for k, v in d:
                self[k] = v
        for k, v in kw.iteritems():
            self[k] = v
