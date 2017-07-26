import heapq
import itertools as it
from listmixin import ListMixin   # (recipe 440656)

__all__ = ['Heap']


class Heap(ListMixin):
    '''A list that maintains the heap invariant.'''

    def __init__(self, iterable=(), key=None):
        '''
        @param iterable: An iterable over items to be added to the heap.
        @param key: Specifies a function of one argument that is used to
            extract a comparison key from each heap element.
        '''
        self._key = key
        self._lst = []
        self.extend(iterable)
        heapq.heapify(self._lst)

    def push(self, item):
        '''Push the item onto the heap.'''
        return heapq.heappush(self._lst, self._wrap(item))

    def popmin(self):
        '''Pop the smallest item off the heap'''
        return self._unwrap(heapq.heappop(self._lst))

    def replace(self, item):
        '''Equivalent to "x = heap.popmin(); heap.push(); return x" but more
        efficient.
        '''
        return self._unwrap(heapq.heapreplace(self._lst, self._wrap(item)))

    def pushpop(self, item):
        'Equivalent to "heap.push(); return heap.popmin()" but more efficient.'
        if self and self[0] < item:
            return self.replace(item)
        return item

    def iterpop(self):
        '''Return a destructive iterator over the heap's elements.

        Each time next is invoked, it pops the smallest item from the heap.
        '''
        while self:
            yield self.popmin()

    #---- overrided ListMixin methods ----------------------------------------

    def constructor(self, iterable):
        return self.__class__(iterable, self._key)

    def __len__(self):
        return len(self._lst)

    def get_element(self, pos):
        return self._unwrap(self._lst[pos])

    def __setitem__(self, pos, item):
        if isinstance(pos, slice):
            raise TypeError('Heap objects do no support slice setting')
        pos = self._fix_index(pos)
        item = self._wrap(item)
        lst = self._lst
        current = lst[pos]
        lst[pos] = item
        if item > current:      # re-establish the heap invariant
            heapq._siftup(lst, pos)
        if lst[pos] != item:    # item found its way below pos
            return
        while pos > 0:
            parentpos = (pos - 1) >> 1
            parent = lst[parentpos]
            if parent <= item:
                break
            lst[pos] = parent
            pos = parentpos
        lst[pos] = item

    def __delitem__(self, pos):
        if isinstance(pos, slice):
            raise TypeError('Heap objects do no support slice deleting')
        pos = self._fix_index(pos)
        lst = self._lst
        if pos == len(lst)-1:
            del lst[-1]
        else:
            self[pos] = self.pop()

    def __iter__(self):
        return it.imap(self._unwrap, self._lst)

    def __nonzero__(self):
        return bool(self._lst)

    def __cmp__(self, other):
        raise TypeError('Heap objects do not support comparison')

    def __eq__(self, other):
        if not isinstance(other,Heap) or len(self) != len(other):
            return False
        for i,j in it.izip(self,other):
            if i != j: return False
        return True

    def __ne__(self,other):
        return not self==other

    def count(self, item):
        return self._lst.count()

    append = push

    def insert(self, pos, item):
        # ignore the position since it's not certain that it can preserve the
        # heap invariant
        self.push(item)

    def extend(self, other):
        if self._key is not None:
            other = it.imap(self._wrap, other)
        push = heapq.heappush; lst = self._lst
        for item in other:
            push(lst,item)

    def sort(self):
        lst = self._lst; pop = heapq.heappop
        sorted = []; append = sorted.append
        while lst:
            append(pop(lst))
        self._lst = sorted

    def reverse(self):
        raise TypeError('Heap objects do not support reversal')

    #---- 'private' methods --------------------------------------------------

    def _wrap(self, item):
        if self._key is not None:
            item = (self._key(item),item)
        return item

    def _unwrap(self, item):
        if self._key is not None:
            item = item[1]
        return item
