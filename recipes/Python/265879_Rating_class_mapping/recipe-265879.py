#
# Rating class with mapping interface
# $Id: rating.py 41 2004-01-14 08:30:59Z hdima $
# Copyright (C) Dmitry Vasiliev <dima at hlabs.spb.ru> 2004
#

__all__ = ["Rating"]

from bisect import bisect_right, bisect_left, insort_left


class RatingItem(object):
    """Rating item

    >>> i = RatingItem("bob", 10)
    >>> i.key, i.value
    ('bob', 10)
    >>> i2 = RatingItem("john", 10)
    >>> i == i2, i < i2, i <= i2, i > i2, i >= i2
    (True, False, True, False, True)
    >>> i2 = RatingItem("paul", 20)
    >>> i == i2, i < i2, i <= i2, i > i2, i >= i2
    (False, True, True, False, False)
    >>> i2 = RatingItem("tom", 0)
    >>> i == i2, i < i2, i <= i2, i > i2, i >= i2 
    (False, False, False, True, True)
    """

    __slots__ = ["key", "value"]

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __cmp__(self, other):
        return cmp(self.value, other.value)

class Rating(object):
    """Rating class with mapping interface

    >>> r = Rating({"bob": 30, "john": 30})
    >>> len(r)
    2
    >>> r.has_key("paul"), "paul" in r
    (False, False)
    >>> r["john"] = 20
    >>> r.update({"paul": 20, "tom": 10})
    >>> len(r)
    4
    >>> r.has_key("paul"), "paul" in r
    (True, True)
    >>> [r[key] for key in ["bob", "john", "paul", "tom"]]
    [30, 20, 20, 10]
    >>> r.get("nobody"), r.get("nobody", 0)
    (None, 0)
    >>> [r.rating(key) for key in ["bob", "john", "paul", "tom"]]
    [3, 2, 1, 0]
    >>> [r.getValueByRating(rating) for rating in range(4)]
    [10, 20, 20, 30]
    >>> [r.getKeyByRating(rating) for rating in range(4)]
    ['tom', 'paul', 'john', 'bob']
    >>> r.keys()
    ['tom', 'paul', 'john', 'bob']
    >>> [key for key in r]
    ['tom', 'paul', 'john', 'bob']
    >>> [key for key in r.iterkeys()]
    ['tom', 'paul', 'john', 'bob']
    >>> r.values()
    [10, 20, 20, 30]
    >>> [value for value in r.itervalues()]
    [10, 20, 20, 30]
    >>> r.items()
    [('tom', 10), ('paul', 20), ('john', 20), ('bob', 30)]
    >>> [item for item in r.iteritems()]
    [('tom', 10), ('paul', 20), ('john', 20), ('bob', 30)]
    >>> r["tom"] = 100
    >>> r.items()
    [('paul', 20), ('john', 20), ('bob', 30), ('tom', 100)]
    >>> del r["paul"]
    >>> r.items()
    [('john', 20), ('bob', 30), ('tom', 100)]
    >>> r["paul"] = 25
    >>> r.items()
    [('john', 20), ('paul', 25), ('bob', 30), ('tom', 100)]
    >>> r.clear()
    >>> r.items()
    []
    """

    __slots__ = ["__dict", "__rating"]

    def __init__(self, mapping=None):
        self.clear()
        if mapping is not None:
            self.update(mapping)

    def update(self, mapping):
        for key, value in mapping.iteritems():
            self.__setitem__(key, value)

    def __len__(self):
        return len(self.__rating)

    def clear(self):
        self.__dict = {}
        self.__rating = []

    def __getitem__(self, key):
        return self.__dict[key].value

    def get(self, key, default=None):
        return self.__dict.get(key, default)

    def __contains__(self, key):
        return key in self.__dict

    has_key = __contains__

    def keys(self):
        return [item.key for item in self.__rating]

    def __iter__(self):
        for item in self.__rating:
            yield item.key

    iterkeys = __iter__

    def values(self):
        return [item.value for item in self.__rating]

    def itervalues(self):
        for item in self.__rating:
            yield item.value

    def items(self):
        return [(item.key, item.value) for item in self.__rating]

    def iteritems(self):
        for item in self.__rating:
            yield item.key, item.value

    def getValueByRating(self, rating):
        return self.__rating[rating].value

    def rating(self, key):
        return self.__getIndexByItem(self.__dict[key])

    def __getIndexByItem(self, item):
        i = bisect_left(self.__rating, item)
        if item is self.__rating[i]:
            return i
        i2 = bisect_right(self.__rating, item) - 1
        if item is self.__rating[i2]:
            return i2
        for i in xrange(i, i2 + 1):
            if item is self.__rating[i]:
                return i
        raise AssertionError("item not found in rating")

    def getKeyByRating(self, rating):
        return self.__rating[rating].key

    def __setitem__(self, key, value):
        if key not in self.__dict:
            item = RatingItem(key, value)
            self.__dict[key] = item
        else:
            item = self.__dict[key]
            del self.__rating[self.__getIndexByItem(item)]
            item.value = value
        insort_left(self.__rating, item)

    def __delitem__(self, key):
        del self.__rating[self.rating(key)], self.__dict[key]

def _test():
    import doctest, rating
    doctest.testmod(rating)

if __name__ == "__main__":
    _test()
