from operator import itemgetter
from heapq import nlargest

class bag(object):

    def __init__(self, iterable=()):
        self._data = {}
        self._len = 0
        self.update(iterable)

    def update(self, iterable):
        if isinstance(iterable, dict):
            for elem, n in iterable.iteritems():
                self[elem] += n
        else:
            for elem in iterable:
                self[elem] += 1 

    def __contains__(self, elem):
        return elem in self._data

    def __getitem__(self, elem):
        return self._data.get(elem, 0)

    def __setitem__(self, elem, n):
        self._len += n - self[elem]
        self._data[elem] = n
        if n == 0:
            del self._data[elem]

    def __delitem__(self, elem):
        self._len -= self[elem]
        del self._data[elem]

    def __len__(self):
        assert self._len == sum(self._data.itervalues())
        return self._len

    def __eq__(self, other):
        if not isinstance(other, bag):
            return False
        return self._data == other._data

    def __ne__(self, other):
        if not isinstance(other, bag):
            return True
        return self._data != other._data

    def __hash__(self):
        raise TypeError

    def __repr__(self):
        return 'bag(%r)' % self._data

    def copy(self):
        return self.__class__(self)

    __copy__ = copy # For the copy module

    def __deepcopy__(self, memo):
        from copy import deepcopy
        result = self.__class__()
        memo[id(self)] = result
        data = result._data
        result._data = deepcopy(self._data, memo)
        result._len = self._len
        return result

    def __getstate__(self):
        return self._data.copy(), self._len

    def __setstate__(self, data):
        self._data = data[0].copy()        
        self._len = data[1]

    def clear(self):
        self._data.clear()
        self._len = 0

    def __iter__(self):
        for elem, cnt in self._data.iteritems():
            for i in xrange(cnt):
                yield elem
                
    def iterunique(self):
        return self._data.iterkeys()

    def itercounts(self):
        return self._data.iteritems()     

    def mostcommon(self, n=None):
        if n is None:
            return sorted(self.itercounts(), key=itemgetter(1), reverse=True)
        it = enumerate(self.itercounts())
        nl = nlargest(n, ((cnt, i, elem) for (i, (elem, cnt)) in it))
        return [(elem, cnt) for cnt, i, elem in nl]
