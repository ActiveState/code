try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping


class IDKeyedMapping(MutableMapping, dict):
    '''A dict that can take mutable objects as keys.'''
    def __len__(self):
        return dict.__len__(self)
    def __iter__(self):
        return dict.__iter__(self)
    def __contains__(self, key):
        return dict.__contains__(self, id(key))
    def __getitem__(self, key):
        return dict.__getitem__(self, id(key))
    def __setitem__(self, key, value):
        dict.__setitem__(self, id(key), value)
    def __delitem__(self, key):
        dict.__delitem__(self, id(key))
    def values(self):
        return dict.values(self)
    def items(self):
        return dict.items(self)
