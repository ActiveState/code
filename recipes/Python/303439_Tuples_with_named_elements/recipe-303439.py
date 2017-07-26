class NamedTuple(tuple):
    """Builds a tuple with elements named and indexed.
    
    A NamedTuple is constructed with a sequence of (name, value) pairs;
    the values can then be obtained by looking up the name or the value.
    """

    def __new__(cls, seq):
        return tuple.__new__(cls, [val for name,val in seq])

    def __init__(self, seq):
        tuple.__init__(self)
        tuple.__setattr__(self, "_names", dict(zip([name for name,val in seq], range(len(seq)))))

    def __getattr__(self, name):
        try:
            return tuple.__getitem__(self, self.__dict__["_names"][name])
        except KeyError:
            raise AttributeError, "object has no attribute named '%s'" % name

    def __setattr__(self, name, value):
        raise TypeError, "'NamedTuple' object has only read-only attributes (assign to .%s)" % name
