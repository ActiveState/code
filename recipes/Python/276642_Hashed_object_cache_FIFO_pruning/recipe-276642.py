# This could much more completely be done as a subclass of dict, but for
# brevity we'll just define it like this for now.

class FifoCache:
    '''
    A mapping(ish) object that remembers the past <entries> items set.
    '''

    def __init__(self, entries):
        self.entries = entries

        self.dct = {}
        self.lst = []

        self.__repr__ = self.dct.__repr__
        self.__contains__ = self.dct.__contains__
        self.__getitem__ = self.dct.__getitem__


    def __setitem__(self, key, value):
        dct = self.dct
        lst = self.lst

        if key in self:
            del self[key]

        lst.append(key)
        dct[key] = value

        if len(lst) > self.entries:
            del dct[lst.pop(0)]


    def __delitem__(self, key):
        if not self.dct.has_key(key):
            raise KeyError, key

        self.lst.remove(key)
        self.dct.pop(key)


# f = FifoCache(entries = 3)
# f["fly"] = "foo"
# f["moo"] = "two"
# f["bar"] = "baz"
# f["dave"] = "wilson"
# f["age"] = 20
# f now has keys 'bar', 'dave', and 'age'.
