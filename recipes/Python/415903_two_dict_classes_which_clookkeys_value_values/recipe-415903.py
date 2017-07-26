class ReverseDict(dict):
    """
    A dictionary which can lookup values by key, and keys by value.
    All values and keys must be hashable, and unique.
    """
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.reverse = dict((reversed(list(i)) for i in self.items()))

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.reverse[value] = key


class LookupDict(dict):
    """
    A dictionary which can lookup values by key, and keys by value.
    The lookup method returns a list of keys with matching values
    to the value argument.
    """
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def lookup(self, value):
        return [item[0] for item in self.items() if item[1] == value]


if __name__ == "__main__":
    a = ReverseDict(((1,2),(3,4)))
    print a[1]
    print a.reverse[2]
    a["123"] = 67
    print a["123"]
    print a.reverse[67]
    print "-" * 20
    b = LookupDict(((1,2),(3,4),(4,2)))
    print b.lookup(2)
