from UserDict import DictMixin


class odict(DictMixin):
    
    def __init__(self):
        self._keys = []
        self._data = {}
        
        
    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value
        
        
    def __getitem__(self, key):
        return self._data[key]
    
    
    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)
        
        
    def keys(self):
        return list(self._keys)
    
    
    def copy(self):
        copyDict = odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict
