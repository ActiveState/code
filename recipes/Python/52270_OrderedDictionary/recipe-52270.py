class OrderedDictionary:

    def __init__(self):

        self._keys=[]
        self._values=[]

    def __len__ (self):
        return len (sef.keys)

    def __getitem__ (self, key):

        if self.has_key (key):
            return self._values[self._keys.index(key)]
        else:
            return None
    def __setitem__ (self, key, value):
        if self.has_key (key):
            self._values [self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def __delitem__(self, key):
        val = self[key]
        
        self._keys.remove(key)
        self._values.remove (val)

    def has_key (self, aKey):
        return aKey in self._keys

    def keys (self):
        return self._keys

    def values (self):
        return self._values

    def items (self):
        return map (None, self._keys, self._values)

    
        
    
        
