def superTuple(name, attributes):
    """Creates a Super Tuple class."""
    dct = {}
    #Create __new__.
    nargs = len(attributes)
    def _new_(cls, *args):
        if len(args) != nargs:
            raise TypeError("%s takes %d arguments (%d given)." % (cls.__name__,
                                                                   nargs,
                                                                   len(args)))
        return tuple.__new__(cls, args)
    dct["__new__"] = staticmethod(_new_)
    #Create __repr__.
    def _repr_(self):
        contents = [repr(elem) for elem in self]
        return "%s<%s>" % (self.__class__.__name__,
                           ", ".join(contents))
    dct["__repr__"] = _repr_
    #Create attribute properties.
    def getter(i):
        return lambda self: self.__getitem__(i)
    for index, attribute in enumerate(attributes):
        dct[attribute] = property(getter(index))
    #Set slots.
    dct["__slots__"] = []
    #Return class.
    return type(name, (tuple,), dct)
