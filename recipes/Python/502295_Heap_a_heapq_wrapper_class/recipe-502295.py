"""
Heap.py -- Heap queue algorithm, class version.
V.1.5, Jan 18 2007, by bearophile

This class provides an implementation of the heap queue algorithm, also known as the
priority queue algorithm, using the heapq standard module.

Heaps are arrays for which heap[k] <= heap[2*k+1] and heap[k] <= heap[2*k+2] for all k,
counting elements from zero. For the sake of comparison, non-existing elements are
considered to be infinite. The interesting property of a heap is that heap[0] is always its
smallest element.

The API below differs from textbook heap algorithms in two aspects: (a) We use zero-based
indexing. This makes the relationship between the index for a node and the indexes for its
children slightly less obvious, but is more suitable since Python uses zero-based indexing.
(b) Our pop method returns the smallest item, not the largest (called a "min heap" in
textbooks; a "max heap" is more common in texts because of its suitability for in-place
sorting).

To create a Heap, you can give it a sequence, or you can create an empty Heap and
popultate it later.

Some doctests:

>>> data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
>>> h = Heap()
>>> bool(h)
False
>>> for item in data:
...     h.push(item)
>>> bool(h)
True
>>> h
Heap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> len(h)
10
>>> h.smallest()
0
>>> 7 in h
True
>>> 10 in h
False
>>> set((h,))
Traceback (most recent call last):
  ...
TypeError: Heap objects are unhashable.
>>> h
Heap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> h.replace(-5)
0
>>> h
Heap([-5, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> h.replace(6)
-5
>>> print h
[1, 2, 3, 4, 5, 6, 6, 7, 8, 9]
>>> h == Heap([1, 3, 2, 6, 6, 5, 4, 7, 8, 9])
True
>>> sorted_data = []
>>> list(h)
[1, 3, 2, 6, 6, 5, 4, 7, 8, 9]
>>> while h:
...     sorted_data.append(h.pop())
...
>>> sorted_data
[1, 2, 3, 4, 5, 6, 6, 7, 8, 9]
>>> h2 = Heap(h)
>>> id(h._heap) == (h2._heap)
False
>>> h == h2
True
>>> h != h2
False
>>> h.clear()
>>> h
Heap()
>>> h = Heap([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
>>> h.popn(4)
[0, 1, 2, 3]
>>> from random import choice
>>> l1 = [choice([0, 0.0]) for _ in xrange(100)]
>>> h1 = Heap(l1)
>>> l2 = [choice([0, 0.0]) for _ in xrange(100)]
>>> h2 = Heap(l2)
>>> h1 == h2
True
>>> h1 > h2
Traceback (most recent call last):
  ...
TypeError: no ordering relation is defined for Heap

>>> h = Heap()
>>> h.push(5)
>>> h.push(1)
>>> h.push(3)
>>> print h, repr(h)
[1, 3, 5] Heap([1, 3, 5])
>>> for el in h: print el
1
5
3
>>> print 2 in h, 3 in h
False True

>>> h = Heap(key=abs)
>>> h.push(-5)
>>> h.push(-1)
>>> h.push(-3)
>>> print h, repr(h)
[-1, -3, -5] Heap([-1, -3, -5])
>>> for el in h: print el
-1
-5
-3
>>> print -2 in h, -3 in h
False True

>>> l = [-1, -3, -5]
>>> h3 = Heap(l, inplace=True)
>>> id(l) == id(h3._heap)
True
>>> l = [-1, -3, -5]
>>> h4 = Heap(l)
>>> id(l) == id(h4._heap)
False
"""

from operator import itemgetter
from heapq import heapify, heappush, heappop, heapreplace, nlargest, nsmallest
from itertools import izip


class Heap(object):
    """Heap(sequence=None, key=None, inplace=False): this class provides an
      implementation of the heap queue algorithm, also known as the priority queue
      algorithm, using the standard heapq module.
    key specifies a function of one argument that is used to extract a comparison key
      from each list element, like the key argument of sort/sorted, ex: key=str.lower
    Use inplace=True if sequence is a list and you want to heapify it in place."""
    def __init__(self, sequence=None, key=None, inplace=False):
        self._key = key
        if key is None:
            if sequence is None:
                self._heap = []
            elif isinstance(sequence, self.__class__) and sequence._key is None:
                self._heap = sequence._heap[:]
            else:
                if inplace and isinstance(sequence, list):
                    self._heap = sequence
                    heapify(self._heap)
                else:
                    self._heap = list(sequence)
                    heapify(self._heap)
            # Replacing them for speed. Is this a problem for the GC?
            self.smallest = self.__smallest_normal
            self.push = self.__push_normal
            self.pop = self.__pop_normal
            self.popn = self.__popn_normal
            self.replace = self.__replace_normal
        else:
            if sequence is None:
                self._heap = []
                self._itemid = 0
            else:
                self._heap = [(key(el), pos, el) for pos, el in enumerate(sequence)]
                heapify(self._heap)
                self._itemid = len(self._heap)
            # Replacing them for speed. Is this a problem for the GC?
            self.smallest = self.__smallest_key
            self.push = self.__push_key
            self.pop = self.__pop_key
            self.popn = self.__popn_key
            self.replace = self.__replace_key

    def __smallest_key(self):
        """smallest(self): return the smalled item of the Heap."""
        return self._heap[0][2]

    def __smallest_normal(self):
        """smallest(self): return the smalled item of the Heap."""
        return self._heap[0]

    def __push_key(self, item):
        """push(item): push the value item onto the heap, maintaining the heap
        invariant."""
        # self._itemid helps to avoid using two times the same id, so they are all
        #   different, so item is never accessed inside __le__
        heappush(self._heap, (self._key(item), self._itemid, item) )
        self._itemid += 1

    def __push_normal(self, item):
        """push(item): push the value item onto the heap, maintaining the heap
        invariant."""
        heappush(self._heap, item)

    def __pop_key(self):
        """pop(): pops and return the smallest item from the heap, maintaining
        the heap invariant. If the heap is empty, IndexError is raised."""
        return heappop(self._heap)[2]

    def __pop_normal(self):
        """pop(): pops and return the smallest item from the heap, maintaining
        the heap invariant. If the heap is empty, IndexError is raised."""
        return heappop(self._heap)

    def __popn_key(self, n):
        """popn(n): pops and return the n smallest items from the heap, maintaining
        the heap invariant. If the heap becomes empty, IndexError is raised."""
        self__heap = self._heap
        return [heappop(self__heap)[2] for _ in xrange(n)]

    def __popn_normal(self, n):
        """popn(n): pops and return the n smallest items from the heap, maintaining
        the heap invariant. If the heap becomes empty, IndexError is raised."""
        self__heap = self._heap
        return [heappop(self__heap) for _ in xrange(n)]

    def __replace_key(self, item):
        """replace(item): pop and return the smallest item from the heap, and also
        push the new item. The heap size doesn't change. If the heap is empty,
        IndexError is raised. This is more efficient than heappop() followed by
        heappush(), and can be more appropriate when using a fixed-size heap. Note
        that the value returned may be larger than item. That constrains reasonable
        uses of this routine unless written as part of a conditional replacement:
            if item > heap[0]:
                item = heapreplace(heap, item)
        """
        return heapreplace(self._heap, (self._key(item), self._itemid, item) )[2]
        self._itemid += 1

    def __replace_normal(self, item):
        """replace(item): pop and return the smallest item from the heap, and also
        push the new item. The heap size doesn't change. If the heap is empty,
        IndexError is raised. This is more efficient than heappop() followed by
        heappush(), and can be more appropriate when using a fixed-size heap. Note
        that the value returned may be larger than item. That constrains reasonable
        uses of this routine unless written as part of a conditional replacement:
            if item > heap[0]:
                item = heapreplace(heap, item)
        """
        return heapreplace(self._heap, item)

    def clear(self):
        """clear(): clears the items of the heap."""
        del self._heap[:]
        if self._key is not None:
            self._itemid = 0

    def __hash__(self):
        raise TypeError("Heap objects are unhashable.")

    def __iter__(self):
        if self._key is None:
            return self._heap.__iter__()
        else:
            return (triple[2] for triple in self._heap)

    def __eq__(self, other):
        if self._key is None:
            return isinstance(other, self.__class__) and \
                sorted(self._heap) == sorted(other._heap)
        else:
            if not isinstance(other, self.__class__) or len(self._heap) != len(other._heap):
                return False
            sorted_self = sorted(self._heap, key=itemgetter(0))
            sorted_other = sorted(other._heap, key=itemgetter(0))
            for (kel1,_,el1), (kel2,_,el2) in izip(sorted_self, sorted_other):
                if kel1 != kel2 or el1 != el2:
                    return False
            return True

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        raise TypeError('no ordering relation is defined for %s' %
                        self.__class__.__name__)

    __gt__ = __le__ = __ge__ = __lt__

    def __len__(self):
        return len(self._heap)

    def __nonzero__(self):
        return bool(self._heap)

    def __str__(self):
        if self._key is None:
            return str(sorted(self._heap))
        else:
            return str( [el[2] for el in sorted(self._heap, key=itemgetter(0))] )

    def __repr__(self):
        if self._heap:
            return "%s(%s)" % (self.__class__.__name__, self)
        else:
            return self.__class__.__name__ + "()"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "Doctests finished."
