""" altsets.py -- An alternate implementation of Sets.py

Implements set operations using sorted lists as the underlying data structure.

Advantages:

  * Space savings -- lists are much more compact than a dictionary
    based implementation.

  * Flexibility -- elements do not need to be hashable, only __cmp__
    is required.

  * Fast operations depending on the underlying data patterns.
    Non-overlapping sets get united, intersected, or differenced
    with only log(N) element comparisons.  Results are built using
    fast-slicing.

  * Algorithms are designed to minimize the number of compares
    which can be expensive.

  * Natural support for sets of sets.  No special accomodation needs to
    be made to use a set or dict as a set member, but users need to be
    careful to not mutate a member of a set since that may breaks its
    sort invariant.

Disadvantages:

  * Set construction uses list.sort() with potentially N log(N)
    comparisons.

  * Membership testing and element addition use log(N) comparisons.
    Element addition uses list.insert() with takes O(N) time.

ToDo:

   * Make the search routine adapt to the data; falling backing to
     a linear search when encountering random data.

"""

from bisect import bisect_left, insort_left

class Set(object):

    def __init__(self, iterable):
        data = list(iterable)
        data.sort()
        result = data[:1]
        for elem in data[1:]:
            if elem == result[-1]:
                continue
            result.append(elem)
        self.data = result
        
    def __repr__(self):
        return 'Set(' + repr(self.data) + ')'

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, elem):
        data = self.data
        i = bisect_left(self.data, elem, 0)
        return i<len(data) and data[i] == elem

    def add(self, elem):
        if elem not in self:
            insort_left(self.data, elem)

    def remove(self, elem):
        data = self.data
        i = bisect_left(self.data, elem, 0)
        if i<len(data) and data[i] == elem:
            del data[i]
 
    def _getotherdata(other):
        if not isinstance(other, Set):
            other = Set(other)
        return other.data
    _getotherdata = staticmethod(_getotherdata)

    def __cmp__(self, other, cmp=cmp):
        return cmp(self.data, Set._getotherdata(other))

    def union(self, other, find=bisect_left):
        i = j = 0
        x = self.data
        y = Set._getotherdata(other)
        result = Set([])        
        append = result.data.append
        extend = result.data.extend
        try:
            while 1:
                if x[i] == y[j]:
                    append(x[i])
                    i += 1
                    j += 1
                elif x[i] > y[j]:
                    cut = find(y, x[i], j)
                    extend(y[j:cut])
                    j = cut
                else:
                    cut = find(x, y[j], i)
                    extend(x[i:cut])
                    i = cut
        except IndexError:
            extend(x[i:])
            extend(y[j:])
        return result

    def intersection(self, other, find=bisect_left):
        i = j = 0
        x = self.data
        y = Set._getotherdata(other)
        result = Set([])        
        append = result.data.append
        try:
            while 1:
                if x[i] == y[j]:
                    append(x[i])
                    i += 1
                    j += 1
                elif x[i] > y[j]:
                    j = find(y, x[i], j)
                else:
                    i = find(x, y[j], i)
        except IndexError:
            pass
        return result
    
    def difference(self, other, find=bisect_left):
        i = j = 0
        x = self.data
        y = Set._getotherdata(other)
        result = Set([])        
        extend = result.data.extend
        try:
            while 1:
                if x[i] == y[j]:
                    i += 1
                    j += 1
                elif x[i] > y[j]:
                    j = find(y, x[i], j)
                else:
                    cut = find(x, y[j], i)
                    extend(x[i:cut])
                    i = cut
        except IndexError:
            extend(x[i:])
        return result

    def symmetric_difference(self, other, find=bisect_left):
        i = j = 0
        x = self.data
        y = Set._getotherdata(other)
        result = Set([])
        extend = result.data.extend
        try:
            while 1:
                if x[i] == y[j]:
                    i += 1
                    j += 1
                elif x[i] > y[j]:
                    cut = find(y, x[i], j)
                    extend(y[j:cut])
                    j = cut
                else:
                    cut = find(x, y[j], i)
                    extend(x[i:cut])
                    i = cut
        except IndexError:
            extend(x[i:])
            extend(y[j:])
        return result


a = Set('abracadabra')
b = Set('alacazam')
print a < b
print a
print b
print map(a.__contains__, list('abcdr'))
print map(a.__contains__, list('0ey'))
print list(a)
print a.union(b), ' :union'
print b.union(a), ' :union'
print a.intersection(b), ' :intersection'
print a.difference(b), ' :difference'
print b.difference(a), ' :difference'
print a.symmetric_difference(b), ' :symmetric_difference'
print b.symmetric_difference(a), ' :symmetric_difference'
print a.intersection(b).union(a.symmetric_difference(b)) == a.union(b)
print a.intersection(b).intersection(a.symmetric_difference(b)) == Set([])
