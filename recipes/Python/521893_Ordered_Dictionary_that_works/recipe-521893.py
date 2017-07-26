class OrderedDict(dict):
    """
    A dictionary in which the insertion order of items is preserved.
    """
    def __init__(self, d={}, **kw):
        self._keys = d.keys() + kw.keys()
        dict.__init__(self, d, **kw)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        # a peculiar sharp edge from copy.deepcopy
        # we'll have our set item called without __init__
        if not hasattr(self, '_keys'):
            self._keys = [key,]
        if key not in self:
            self._keys.append(key)
        dict.__setitem__(self, key, item)

    def clear(self):
        dict.clear(self)
        self._keys = []

    def popitem(self):
        if len(self._keys) == 0:
            raise KeyError('dictionary is empty')
        else:
            key = self._keys[-1]
            val = self[key]
            del self[key]
            return key, val

    def setdefault(self, key, failobj = None):
        if key not in self:
            self._keys.append(key)
        dict.setdefault(self, key, failobj)

    def update(self, d):
        for key in d.keys():
            if not self.has_key(key):
                self._keys.append(key)
        dict.update(self, d)

    def iterkeys(self):
        return iter(self._keys)

    def keys(self):
        return self._keys[:]

    def itervalues(self):
        for k in self._keys:
            yield self[k]

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        for k in self._keys:
            yield k, self[k]

    def items(self):
        return list(self.iteritems())

    def __iter__(self):
        return self.iterkeys()

    def index(self, key):
        if not self.has_key(key):
            raise KeyError(key)
        return self._keys.index(key)
