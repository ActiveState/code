"""
odict.py  -- V.1.1, Oct 12 2006, by bearophile.

Dictionary in which the *insertion* order of items is preserved (using an internal double
linked list). In this implementation replacing an existing item keeps it at its original
position.
Requires Python V.2.4 or successive.

Note: I have removed the doctstrings from most methods to make this code shorter for
the cookbook.

Internal representation: values of the dict:
  +-----------+----------+-----------+
  | <pred key | true val | succ key> |
  +-----------+----------+-----------+
The sequence of elements uses as a double linked list. The 'links' are dict keys.
  self.lh and self.lt are the keys of first and last element inseted in the Odict.
In a C reimplementation of this data structure, things can be simplified (and speed
  up) a lot if given a value you can at the same time find its key. With that, you
  can use normal C pointers.

Memory used (Python 2.5):
set(int): 28.2 bytes/element
dict(int:None): 36.2 bytes/element
Odict(int:None): 102 bytes/element

Speed:
- This Odict is about 20-25 times slower than a dict, for insert and del operations.
- del too is O(1).
"""

class _Nil:
    """Class of the 'pointer' to the null key. For internal usage only."""
    def __repr__(self): # Useful for Odict._repr()
        return "nil"

_nil = _Nil() # 'Pointer' to the null key.

class Odict(dict):
    """
    Ordered dict data structure, with O(1) complexity for dict operations
    that modify one element.
    Overwriting values doesn't change their original sequential order."""
    def __init__(self, data=(), **kwds):
        """This doesn't accept keyword initialization as normal dicts to avoid a trap:
        inside a function or method the keyword args are accessible only as a dict,
        without a defined order, so their original order is lost.

        __init__ test, with keyword args:
        >>> Odict(a=1)
        Traceback (most recent call last):
          ...
        TypeError: __init__() of ordered dict takes no keyword arguments to avoid an ordering trap.

        If initialized with a dict the order of elements is undefined!:
        >>> o = Odict({"a":1, "b":2, "c":3, "d":4})
        >>> print o
        {'a': 1, 'c': 3, 'b': 2, 'd': 4}
        """
        if kwds:
            raise TypeError("__init__() of ordered dict takes no keyword arguments to"
                            " avoid an ordering trap.")
        dict.__init__(self)
        self.lh = _nil # Double-linked list header
        self.lt = _nil # Double-linked list tail
        # If you give a normal dict, then the order of elements is undefined
        if hasattr(data, "iteritems"):
            for key, val in data.iteritems():
                self[key] = val
        else:
            for key, val in data:
                self[key] = val

    def __getitem__(self, key):
        return dict.__getitem__(self, key)[1]

    def __setitem__(self, key, val):
        if key in self:
            dict.__getitem__(self, key)[1] = val
        else:
            new = [self.lt, val, _nil]
            dict.__setitem__(self, key, new)
            if self.lt is _nil:
                self.lh = key
            else:
                dict.__getitem__(self, self.lt)[2] = key
            self.lt = key

    def __delitem__(self, key):
        """
        del test 1, removal from empty Odict:
        >>> o = Odict()
        >>> del o["1"]
        Traceback (most recent call last):
          ...
        KeyError: '1'

        del test 2, removal from Odict with one element:
        >>> o = Odict()
        >>> o["1"] = 1
        >>> del o["1"]
        >>> o.lh, o.lt, o, o
        (nil, nil, Odict(), Odict())
        >>> o._repr()
        'Odict low level repr lh,lt,data: nil, nil, {}'

        del test 3, removal firt element of the Odict sequence:
        >>> o = Odict()
        >>> for i in [1,2,3]: o[str(i)] = i
        >>> del o["1"]
        >>> o.lh, o.lt, o
        ('2', '3', Odict([('2', 2), ('3', 3)]))

        del test 4, removal element in the middle of the Odict sequence:
        >>> o = Odict()
        >>> for i in [1,2,3]: o[str(i)] = i
        >>> del o["2"]
        >>> o.lh, o.lt, o
        ('1', '3', Odict([('1', 1), ('3', 3)]))

        del test 5, removal element at the end of the Odict sequence:
        >>> o = Odict()
        >>> for i in [1,2,3]: o[str(i)] = i
        >>> del o["3"]
        >>> o.lh, o.lt, o
        ('1', '2', Odict([('1', 1), ('2', 2)]))
        """
        if key in self:
            pred, _ ,succ= dict.__getitem__(self, key)
            if pred is _nil:
                self.lh = succ
            else:
                dict.__getitem__(self, pred)[2] = succ
            if succ is _nil:
                self.lt = pred
            else:
                dict.__getitem__(self, succ)[0] = pred
            dict.__delitem__(self, key)
        else:
            raise KeyError, key

    def __str__(self):
        pairs = ("%r: %r" % (k, v) for k, v in self.iteritems())
        return "{%s}" % ", ".join(pairs)

    def __repr__(self):
        if self:
            pairs = ("(%r, %r)" % (k, v) for k, v in self.iteritems())
            return "Odict([%s])" % ", ".join(pairs)
        else:
            return "Odict()"

    def get(self, k, x=None):
        if k in self:
            return dict.__getitem__(self, k)[1]
        else:
            return x

    def __iter__(self):
        curr_key = self.lh
        while curr_key is not _nil:
            yield curr_key
            curr_key = dict.__getitem__(self, curr_key)[2]

    iterkeys = __iter__

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        curr_key = self.lh
        while curr_key is not _nil:
            _, val, curr_key = dict.__getitem__(self, curr_key)
            yield val

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        curr_key = self.lh
        while curr_key is not _nil:
            _, val, next_key = dict.__getitem__(self, curr_key)
            yield curr_key, val
            curr_key = next_key

    def items(self):
        return list(self.iteritems())

    def clear(self):
        dict.clear(self)
        self.lh = _nil
        self.lt = _nil

    def copy(self):
        return self.__class__(self)

    def update(self, data=(), **kwds):
        if kwds:
            raise TypeError("update() of ordered dict takes no keyword arguments"
                            " to avoid an ordering trap.")
        if hasattr(data, "iteritems"):
            for key, val in data.iteritems():
                self[key] = val
        else:
            for key, val in data:
                self[key] = val

    @classmethod
    def fromkeys(cls, seq, value=None):
        new = cls()
        for key in seq:
            new[key] = value
        return new

    def setdefault(self, k, x=None):
        if k in self:
            return self[k]
        else:
            self[k] = x
            return x

    def pop(self, k, x=_nil):
        if k in self:
            val = self[k]
            del self[k]
            return val
        elif x is _nil:
            raise KeyError(k)
        else:
            return x

    def popitem(self):
        if self:
            key = self.lt
            val = dict.__getitem__(self, key)[1]
            self.__delitem__(key)
            return key, val
        else:
            raise KeyError("'popitem(): ordered dictionary is empty'")

    # Some Odict-specific methods ---------------------------------
    def riterkeys(self):
        """To iterate on keys in reversed order."""
        curr_key = self.lt
        while curr_key is not _nil:
            yield curr_key
            curr_key = dict.__getitem__(self, curr_key)[0]

    __reversed__ = riterkeys

    def rkeys(self):
        """List of the keys in reversed order."""
        return list(self.riterkeys())

    def ritervalues(self):
        """To iterate on values in reversed order."""
        curr_key = self.lt
        while curr_key is not _nil:
            curr_key, val, _ = dict.__getitem__(self, curr_key)
            yield val

    def rvalues(self):
        """List of the values in reversed order."""
        return list(self.ritervalues())

    def riteritems(self):
        """To iterate on (key, value) in reversed order."""
        curr_key = self.lt
        while curr_key is not _nil:
            pred_key, val, _ = dict.__getitem__(self, curr_key)
            yield curr_key, val
            curr_key = pred_key

    def ritems(self):
        """List of the (key, value) in reversed order."""
        return list(self.riteritems())

    def firstkey(self):
        if self:
            return self.lh
        else:
            raise KeyError("'firstkey(): ordered dictionary is empty'")

    def lastkey(self):
        if self:
            return self.lt
        else:
            raise KeyError("'lastkey(): ordered dictionary is empty'")

    def _repr(self):
        """_repr(): low level repr of the whole data contained in the Odict.
        Useful for debugging."""
        form = "Odict low level repr lh,lt,data: %r, %r, %s"
        return form % (self.lh, self.lt, dict.__repr__(self))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "Tests done."
