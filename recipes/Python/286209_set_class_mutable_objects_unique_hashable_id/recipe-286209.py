class KeyedSet(dict):

    """
    A set class for handling collections of arbitrary
    objects that have unique, and hashable 'id' attributes.
    Set items are stored as values in a dictionary, with ids
    as keys.  There is no requirement for set items to be hashable.
    The class requires a 1 to 1 mapping between objects
    and their ids, and is designed for cases where access to
    items via a key lookup is also desirable.
    """

    def __init__(self, items=None):
        if items is not None:
            for item in items:
                self[item.id] = item

    def add(self, item):
        self[item.id] = item

    def remove(self, item):
        del self[item.id]

    def __contains__(self, item):
        try:
            return self.has_key(item.id)
        except AttributeError:
            return False

    def __iter__(self):
        return self.itervalues()

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.keys())

    def __cmp__(self, other):
        raise TypeError, "can't compare KeyedSets using cmp()"

    def issubset(self, other):
        self._binary_check(other)
        if len(self) > len(other):
            return False
        else:
            for key in self.iterkeys():
                if not other.has_key(key):
                    return False
        return True

    def issuperset(self, other):
        self._binary_check(other)
        return other.issubset(self)

    __le__ = issubset
    __ge__ = issuperset

    def __lt__(self, other):
        self._binary_check(other)
        return len(self) < len(other) and self.issubset(other)

    def __gt__(self, other):
        self._binary_check(other)
        return len(self) > len(other) and self.issuperset(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self) == len(other) and self.issubset(other)
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        else:
            return True

    def union(self, other):
        res = self.copy()
        for item in other:
            res.add(item)
        return res

    def intersection(self, other):
        res = self.__class__()
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        if len(self) > len(other):
            for item in other:
                if item in self:
                    res.add(item)
        else:
            for item in self:
                if item in other:
                    res.add(item)
        return res

    def difference(self, other):
        res = self.copy()
        for item in other:
            if item in res:
                res.remove(item)
        return res

    def symmetric_difference(self, other):
        res = self.copy()
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        for item in other:
            if item in self:
                res.remove(item)
            else:
                res.add(item)
        return res

    def __or__(self, other):
        self._binary_check(other)
        return self.union(other)

    def __and__(self, other):
        self._binary_check(other)
        return self.intersection(other)

    def __sub__(self, other):
        self._binary_check(other) 
        return self.difference(other)

    def __xor__(self, other):
        self._binary_check(other)
        return self.symmetric_difference(other)

    def _binary_check(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError, "Binary operation only permitted between KeyedSets"

    def copy(self):
        res = self.__class__()
        res.update(self)
        return res

    def union_update(self, other):
        if isinstance(other, (self.__class__, dict)):
            self.update(other)
        else:
            for item in other:
                self.add(item)

    def intersection_update(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self &= other

    def difference_update(self, other):
        for item in other:
            self.discard(item)

    def symmetric_difference_update(self, other):
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        for item in other:
            if item in self:
                self.remove(item)
            else:
                self.add(item)

    def __ior__(self, other):
        self._binary_check(other)
        self.union_update(other)
        return self

    def __iand__(self, other):
        self._binary_check(other)
        intersect = self & other
        self.clear()
        self.update(intersect)
        return self

    def __isub__(self, other):
        self._binary_check(other)
        self.difference_update(other)
        return self

    def __ixor__(self, other):
        self._binary_check(other)
        self.symmetric_difference_update(other)
        return self

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def pop(self, *args):
        if args:
            return super(self.__class__, self).pop(*args)
        else:
            return self.popitem()[1]

    def update(self, other):
        if isinstance(other, (self.__class__, dict)):
            super(self.__class__, self).update(other)
        else:
            for item in other:
                self.add(item)
