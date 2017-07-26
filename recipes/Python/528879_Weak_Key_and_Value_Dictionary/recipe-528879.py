# By Eyal Lotem and Yair Chuchem, 2007

import weakref

class WeakKeyValueDict(object):
    """
    A dict in which items are removed whenever either key or value are
    garbage-collected.
    """
    def __init__(self, *args, **kw):
        init_dict = dict(*args, **kw)
        
        self._d = weakref.WeakKeyDictionary(
            (key, self._create_value(key, value))
            for key, value in init_dict.iteritems())

    def _create_value(self, key, value):
        key_weakref = weakref.ref(key)
        def value_collected(wr):
            del self[key_weakref()]
        return weakref.ref(value, value_collected)

    def __getitem__(self, key):
        return self._d[key]()
    
    def __setitem__(self, key, value):
        self._d[key] = self._create_value(key, value)

    def __delitem__(self, key):
        del self._d[key]

    def __len__(self):
        return len(self._d)

    def __cmp__(self, other):
        try:
            other_iteritems = other.iteritems
        except AttributeError:
            return NotImplemented
        return cmp(sorted(self.iteritems()),
                   sorted(other_iteritems()))

    def __hash__(self):
        raise TypeError("%s objects not hashable" % (self.__class__.__name__,))

    def __contains__(self, key):
        return key in self._d

    def __iter__(self):
        return self.iterkeys()

    def iterkeys(self):
        return self._d.iterkeys()

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        for value in self._d.itervalues():
            yield value()

    def values(self):
        return list(self.itervalues())
    
    def iteritems(self):
        for key in self._d:
            yield self._d[key]()

    def items(self):
        return list(self.iteritems())

    def update(self, other):
        for key, value in other.iteritems():
            self[key] = value

    def __repr__(self):
        return repr(self._d)

    def clear(self):
        self._d.clear()

    def copy(self):
        return WeakKeyValueDict(self)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def has_key(self, key):
        return key in self

    def pop(self, key, *args):
        if args:
            return self._pop_with_default(key, *args)
        return self._pop(key)

    def _pop(self, key):
        return self._d.pop(key)()
    
    def _pop_with_default(self, key, default):
        if key in self:
            return self._d.pop(key)
        return default

    def popitem(self):
        key, value = self._d.popitem()
        return key, value()

    def setdefault(self, key, default):
        if key in self:
            return self[key]
        self[key] = default
        return default
