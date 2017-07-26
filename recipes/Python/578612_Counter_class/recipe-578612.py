# This file is part of PanGaia and licensed under the CreativeCommons, Share-Alike, Attribution
# (C) Mark Janssen, dreamingforward@gmail.com
# For most up-to-date version, see the PangaiaProject 

"""Bag types:  a set-like container that counts the number of the same items held within it."""

import random  #pick()

_DEBUG = True

class IntegerBag(dict):
    """Implements a bag type that allows item counts to be negative."""

    __slots__ = []

    def __init__(self, init={}):
        """Initialize bag with optional contents.

        >>> b = Bag()   #creates empty bag
        >>> b
        {}
        >>> print(IntegerBag({1: -1, 2: 0, 3: -9}))
        {1: -1, 3: -9}

        Can initialize with (key, count) list as in standard dict.
        However, duplicate keys will accumulate counts:
        >>> print(Bag([(1, 2), (2, 4), (1, 7)]))
        {1: 9, 2: 4}
        """
        if not init or isinstance(init, self.__class__):
            dict.__init__(self, init)   #values known to be good, use faster dict creation
        else:   #initializing with list or plain dict
            dict.__init__(self)
            if isinstance(init, dict):
                for key, count in init.items():
                    self[key] = count #will test invariants
            else:       #sequence may contain duplicates, so add to existing value, if any
                for key, count in init:
                    self[key] += count

    def fromkeys(cls, iterable, count=1):
        """Class method which creates bag from iterable adding optional count for each item.

        >>> b = Bag({'b': 2, 'c': 1, 'a': 3})
        >>> b2 = Bag.fromkeys(['a', 'b', 'c', 'b', 'a', 'a'])
        >>> b3 = Bag.fromkeys("abacab")
        >>> assert b == b2 == b3

        >>> word_count = Bag.fromkeys("how much wood could a wood chuck chuck".split())
        >>> print(word_count)
        {'a': 1, 'chuck': 2, 'could': 1, 'how': 1, 'much': 1, 'wood': 2}

        An optional count can be specified.  Count added each time item is encountered.
        >>> print(Bag.fromkeys("abacab", 5))
        {'a': 15, 'b': 10, 'c': 5}
        """
        b = cls()
        for key in iterable: #could just return b.__iadd__(iterable, count)
            b[key] += count  #perhaps slower than necessary but will simplify derived classes that override __setitem__()
        return b

    fromkeys = classmethod(fromkeys)

    def update(self, items, count=1):
        """Adds contents to bag from other mapping type or iterable.

        >>> ib = IntegerBag.fromkeys('abc')
        >>> ib.update({'a': 2, 'b': 1, 'c': 0})
        >>> print(ib)
        {'a': 3, 'b': 2, 'c': 1}

        Negative updates are allowable.
        >>> ib.update({'a': -2, 'b': -2, 'c': -2, 'd': 2})
        >>> print(ib)
        {'a': 1, 'c': -1, 'd': 2}

        Can call with iterable.  Amount added can be specified by count parameter:
        >>> ib.update(['a','b'], 2)
        >>> print(ib)
        {'a': 3, 'b': 2, 'c': -1, 'd': 2}

        Values that can't be converted to ints are skipped and will raise TypeError.
        >>> ib.update({0: 'test1', 'a': 'test2', 'd': 3, 'f': '1.0', 'c': 2.0})
        Traceback (most recent call last):
        TypeError: unsupported operand type(s) for +=: 'int' and 'str'
        >>> print(ib)
        {'a': 3, 'b': 2, 'c': 1, 'd': 5}

        Updating Bag with values that would cause the count to go negative
        sets count to 0, removing item.
        >>> b = Bag({'a': 1, 'c': 2, 'd': 5})
        >>> b.update({'a': -4, 'b': -1, 'c': -2, 'd': -2})
        >>> print(b)
        {'d': 3}

        NOTE:  Exceptions are only reported on the last bad element encountered.
        """
        #XXX may be able to improve this by calling dict methods directly and/or using map and operator functions
        #XXX should raise exception and return unchanged self if problem encountered!
        #XXX or use logging.warning() and continue
        err = False
        if isinstance(items, dict):
            for key, count in items.items():
                try:
                    self[key] += count  #may be slower than necessary
                except TypeError as error: err = True #FIXME should have to re-assign to propagate error:  check docs
        else: #sequence
            for key in items:
                try:
                    self[key] += count
                except TypeError as error: err = Trie
        if err: raise TypeError(error)

    def pick(self, count=1, remove=True): #XXX perhaps better to default to False?
        """Returns a bag with 'count' random items from bag (defaults to 1), removing the items unless told otherwise.

        >>> b = IntegerBag({'a': 3, 'b': -2, 'c': 1})
        >>> sub = b.pick(4)
        >>> sub.size, b.size
        (4, 2)
        """
        l = list(self.itereach())
        picked = IntegerBag(random.sample(l, min(abs(count), len(l))))
        if count < 0:  picked *= (-1)  #this probably not useful except for Network class
        if remove: self -= picked
        return picked

    def pop(self, item):
        """Remove all of item from bag, returning its count, if any.

        >>> b = IntegerBag.fromkeys("abacab")
        >>> b.pop('b')
        2
        >>> b.pop('z')
        0
        >>> print(b)
        {'a': 3, 'c': 1}
        """
        return super(IntegerBag, self).pop(item, 0)

    def discard(self, item):
        """Removes all of the specified item if it exists, otherwise ignored.

        >>> b = Bag.fromkeys("abacab")
        >>> b.discard('b')
        >>> b.discard('d')  #non-existent items ignored
        >>> print(b)
        {'a': 3, 'c': 1}
        """
        try: del self[item] #note: this does not call __getitem__
        except KeyError: pass

    def setdefault(self, item, count=1):
        count = self._filter(count)
        return count and dict.setdefault(self, item, count)

    def itereach(self):  #XXX consider rename akin to Python3 rules
        """Will iterate through all items in bag individually.

        >>> b = Bag.fromkeys("abacab")
        >>> l = list(b.itereach()); l.sort()
        >>> l
        [('a', 1), ('a', 1), ('a', 1), ('b', 1), ('b', 1), ('c', 1)]
        >>> b = IntegerBag(b)
        >>> b['b'] = -2
        >>> l = list(b.itereach()); l.sort()
        >>> l
        [('a', 1), ('a', 1), ('a', 1), ('b', -1), ('b', -1), ('c', 1)]

        Note: iteration on bag itself just iterates through unique keys:
        >>> l = list(b) ; l.sort()
        >>> l
        ['a', 'b', 'c']
        """
        for key, count in self.items():
            for i in range(abs(count)):
                yield (key, count >= 0 and 1 or -1) #consider returning (key, +/-1) pair to account for negative counts

    def __iadd__(self, other):
        """Add items in bag.

        >>> b = Bag()
        >>> b += [1, 2, 1, 0]
        >>> print(b)
        {0: 1, 1: 2, 2: 1}
        >>> b.clear()
        >>> b += "abca"
        >>> print(b)
        {'a': 2, 'b': 1, 'c': 1}
        """
        self.update(other, 1)  #XXX may fail mid-update...
        return self

    def __add__(self, other):  #XXX better way to create copy?? (in case self.__class__ has more complicated constructor...)
        """Add one bag to another, returns type of first bag.

        >>> b = IntegerBag({1: 2, 2: -2}) + Bag({1: 5, 2: 1, 3: 7})
        >>> b, "IntegerBag" in str(type(b))
        ({1: 7, 2: -1, 3: 7}, True)
        """
        return self.__class__(self).__iadd__(other)

    def __isub__(self, other):
        """Subtract items from bag.

        >>> b = Bag.fromkeys("abacab")
        >>> b -= "cccccab"
        >>> print(b)
        {'a': 2, 'b': 1}
        """
        if isinstance(other, dict):
            other = IntegerBag(other) * (-1)
        self.update(other, -1)
        return self

    def __sub__(self, other):
        """Subtract items from bag.

        >>> IntegerBag({1: 2, 2: -2}) - {1: 5, 2: -2, 3: 7}
        {1: -3, 3: -7}
        """
        return self.__class__(self).__isub__(other)

    def __imul__(self, factor):
        """Multiply bag contents by factor.

        >>> b = Bag.fromkeys("abacab")
        >>> b *= 4
        >>> print(b)
        {'a': 12, 'b': 8, 'c': 4}

        Negative factors can be used with IntegerBag.
        >>> ib = IntegerBag(b)
        >>> ib *= -1
        >>> print(ib)
        {'a': -12, 'b': -8, 'c': -4}

        Trying that on a Bag will return empty bag (akin to list behavior).
        >>> b *= -1
        >>> b
        {}

        Zero factors will return empty bag.
        >>> b += "abacab"
        >>> b *= 0
        >>> b
        {}

        """
        if self._filter(factor):
            for item, count in self.items():
                dict.__setitem__(self, item, count*factor) #bypass test logic in bag.__setitem__
        else:   #factor==0 or negative on Bag
            dict.clear(self)    #call dict.clear to protect subclass which might override and do other things besides clear dict values
        return self

    def __mul__(self, factor):
        """Returns new bag of same type multiplied by factor.

        >>> d = {1: 2, 2: 4, 3: -9}
        >>> IntegerBag(d) * -1
        {1: -2, 2: -4, 3: 9}
        >>> Bag(d) * -1
        {}
        """
        #XXX should perhaps use explicit IntBag in case derived class needs parameters -- or use copy()???
        return self.__class__(self).__imul__(factor)

    def _size(self):
        """Returns sum of absolute value of item counts in bag.

        >>> b = IntegerBag.fromkeys("abacab")
        >>> b['a'] = -4
        >>> b.size
        7
        """
        return sum(map(abs, self.values()))

    size = property(_size, None, None, "Sum of absolute count values in the bag")

    def __getitem__(self, item):
        """Returns total count for given item, or zero if item not in bag.

        >>> b = Bag.fromkeys("abacab")
        >>> b['a']
        3
        >>> b['d']
        0
        """
        return self.get(item, 0)

    count = __getitem__

    def __setitem__(self, item, count):
        """Sets the count for the given item in bag, removing if zero.

        >>> b = Bag()
        >>> b[1] = 3
        >>> b[3] = 1.6  #floats get coerced to ints
        >>> b[4] = "2"  #as do int strings
        >>> print(b)
        {1: 3, 3: 1, 4: 2}

        If count is zero, all 'matching items' are deleted from bag.
        >>> b[2] = 0
        >>> print(b)
        {1: 3, 3: 1, 4: 2}

        Counts for IntegerBag are allowed to be negative.
        >>> ib = IntegerBag(b)
        >>> ib[4] = -2
        >>> ib[5] -= 2
        >>> ib[1] -= 4
        >>> ib[3] -= 1
        >>> print(ib)
        {1: -1, 4: -2, 5: -2}

        Trying to set negative values on Bag reverts to zero.
        >>> b[4] = -2
        >>> b[4]
        0

        If count is non-integer, an exception is raised.
        >>> b[1] = "oops"  #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: invalid literal for int(): oops
        """
        count = self._filter(count)
        if count:
            dict.__setitem__(self, item, count)  #XXX should this call super instead of dict (for cases of multiple inheritence etc...)
        else:   #setting to 0 so discard key
            self.discard(item)

    def __str__(self):
        """Convert self to string with items in sorted order.

        >>> str(IntegerBag())
        '{}'
        >>> str(IntegerBag({'b': -2, 'a': 3, 'c': 1, 1: 0}))
        "{'a': 3, 'b': -2, 'c': 1}"
        >>> str(Bag.fromkeys("abacab"))
        "{'a': 3, 'b': 2, 'c': 1}"
        """
        #sort by values, largest first? should we sort at all?
        if _DEBUG: self._validate()
        if not self: return '{}'    #nothing to sort
        keys = sorted(self) #this extra assigment necessary???  !Must remember basic python!...
        return '{%s}' % ', '.join(["%r: %r" % (k, self[k]) for k in keys])

    def _filter(value): #XXX could just set _filter = int but doctest complains even under Python 2.3.3
        """Coerces value to int and returns it, or raise raises TypeError."""
        return int(value)

    _filter = staticmethod(_filter)

    def _validate(self):
        """Check class invariants.

        >>> b = IntegerBag.fromkeys("abc")
        >>> dict.__setitem__(b, 'a', "oops")
        >>> b._validate() #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: invalid literal for int(): oops
        >>> b = Bag()
        >>> dict.__setitem__(b, 'a', 0)    #zero values are normally deleted
        >>> b
        {'a': 0}
        >>> b._validate()
        Traceback (most recent call last):
        AssertionError: zero value encountered
        >>> b = Bag()
        >>> dict.__setitem__(b, 'a', -1)   #negative values not allowed
        >>> b._validate()
        Traceback (most recent call last):
        AssertionError: unfiltered value
        """
        for count in self.values():
            assert count == self._filter(count), "unfiltered value"
            assert count, "zero value encountered"


class Bag(IntegerBag):
    """Standard bag class.  Allows only non-negative bag counts."""

    __slots__ = []

    def _size(self):
        """Returns total number of items in bag.

        >>> b = Bag.fromkeys("abacab")
        >>> b.size
        6
        """
        return sum(self.values())

    size = property(_size, None, None, "Sum of all bag values.")

    def _filter(value):
        """Returns 0 if value is negative. """
        return max(int(value), 0)

    _filter = staticmethod(_filter)


def _test():
    """Miscillaneous tests:

    Equality test.  Can compare against dictionary or bag types.
    >>> Bag.fromkeys("abacab") == {'a': 3, 'b': 2, 'c': 1}
    True
    >>> b, l = Bag.fromkeys([1, 2, 1, 3, 1]), [1, 1, 1, 3, 2]
    >>> b == l
    False
    >>> b == Bag.fromkeys(l) == IntegerBag.fromkeys(l)
    True

    Tests for non-zero:
    >>> b = Bag()
    >>> bool(b)
    False
    >>> b += [0]
    >>> bool(b)
    True
    """
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test(), throws the bird in the incinerator and bolts out of the room, fear of being found. 
