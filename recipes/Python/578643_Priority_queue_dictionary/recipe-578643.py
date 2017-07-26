from collections import MutableMapping

class _MinEntry(object):
    """
    Mutable entries for a Min-PQ dictionary.

    """
    def __init__(self, dkey, pkey):
        self.dkey = dkey    #dictionary key
        self.pkey = pkey    #priority key

    def __lt__(self, other):
        return self.pkey < other.pkey

class _MaxEntry(object):
    """
    Mutable entries for a Max-PQ dictionary.

    """
    def __init__(self, dkey, pkey):
        self.dkey = dkey
        self.pkey = pkey

    def __lt__(self, other):
        return self.pkey > other.pkey

class PQDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._heap = []
        self._position = {}
        self.update(*args, **kwargs)

    create_entry = _MinEntry     #defaults to a min-pq
    @classmethod
    def maxpq(cls, *args, **kwargs):
        pq = cls()
        pq.create_entry = _MaxEntry
        pq.__init__(*args, **kwargs)
        return pq

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        for entry in self._heap:
            yield entry.dkey

    def __getitem__(self, dkey):
        return self._heap[self._position[dkey]].pkey

    def __setitem__(self, dkey, pkey):
        heap = self._heap
        position = self._position

        try:
            pos = position[dkey]
        except KeyError:
            # Add a new entry:
            # put the new entry at the end and let it bubble up
            pos = len(self._heap)
            heap.append(self.create_entry(dkey, pkey))
            position[dkey] = pos
            self._swim(pos)
        else:
            # Update an existing entry:
            # bubble up or down depending on pkeys of parent and children
            heap[pos].pkey = pkey
            parent_pos = (pos - 1) >> 1
            child_pos = 2*pos + 1
            if parent_pos > -1 and heap[pos] < heap[parent_pos]:
                self._swim(pos)
            elif child_pos < len(heap):
                other_pos = child_pos + 1
                if other_pos < len(heap) and not heap[child_pos] < heap[other_pos]:
                    child_pos = other_pos
                if heap[child_pos] < heap[pos]:
                    self._sink(pos)

    def __delitem__(self, dkey):
        heap = self._heap
        position = self._position

        pos = position.pop(dkey)
        entry_to_delete = heap[pos]

        # Take the very last entry and place it in the vacated spot. Let it
        # sink or swim until it reaches its new resting place.
        end = heap.pop(-1)
        if end is not entry_to_delete:
            heap[pos] = end
            position[end.dkey] = pos
            parent_pos = (pos - 1) >> 1
            child_pos = 2*pos + 1
            if parent_pos > -1 and heap[pos] < heap[parent_pos]:
                self._swim(pos)
            elif child_pos < len(heap):
                other_pos = child_pos + 1
                if other_pos < len(heap) and not heap[child_pos] < heap[other_pos]:
                    child_pos = other_pos
                if heap[child_pos] < heap[pos]:
                    self._sink(pos)
        del entry_to_delete

    def peek(self):
        try:
            entry = self._heap[0]
        except IndexError:
            raise KeyError
        return entry.dkey, entry.pkey

    def popitem(self):
        heap = self._heap
        position = self._position

        try:
            end = heap.pop(-1)
        except IndexError:
            raise KeyError

        if heap:
            entry = heap[0]
            heap[0] = end
            position[end.dkey] = 0
            self._sink(0)
        else:
            entry = end
        del position[entry.dkey]
        return entry.dkey, entry.pkey

    def iteritems(self):    
        # destructive heapsort iterator
        try:
            while True:
                yield self.popitem()
        except KeyError:
            return

    def _sink(self, top=0):
        # "Sink-to-the-bottom-then-swim" algorithm (Floyd, 1964)
        # Tends to reduce the number of comparisons when inserting "heavy" items
        # at the top, e.g. during a heap pop
        heap = self._heap
        position = self._position

        # Grab the top entry
        pos = top
        entry = heap[pos]
        # Sift up a chain of child nodes
        child_pos = 2*pos + 1
        while child_pos < len(heap):
            # choose the smaller child
            other_pos = child_pos + 1
            if other_pos < len(heap) and not heap[child_pos] < heap[other_pos]:
                child_pos = other_pos
            child_entry = heap[child_pos]
            # move it up one level
            heap[pos] = child_entry
            position[child_entry.dkey] = pos
            # next level
            pos = child_pos
            child_pos = 2*pos + 1
        # We are left with a "vacant" leaf. Put our entry there and let it swim 
        # until it reaches its new resting place.
        heap[pos] = entry
        position[entry.dkey] = pos
        self._swim(pos, top)

    def _swim(self, pos, top=0):
        heap = self._heap
        position = self._position

        # Grab the entry from its place
        entry = heap[pos]
        # Sift parents down until we find a place where the entry fits.
        while pos > top:
            parent_pos = (pos - 1) >> 1
            parent_entry = heap[parent_pos]
            if not entry < parent_entry:
                break
            heap[pos] = parent_entry
            position[parent_entry.dkey] = pos
            pos = parent_pos
        # Put entry in its new place
        heap[pos] = entry
        position[entry.dkey] = pos
