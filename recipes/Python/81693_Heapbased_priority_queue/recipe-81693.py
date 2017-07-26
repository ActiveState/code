class PriQueue:
    """Least-first priority queue (elements must be comparable).

    To use another ordering, fix the three places marked # comparison.
    q=PriQueue(lst) Creates a priority queue with all entries in list
    i=len(q)      count of values in queue
    q.push(v)     Add entry to queue
    vb=q.cream(v) Add v to queue, and then remove and return the least entry.
    v=q.top()     view least entry in queue
    v=q.pop()     remove and return least entry in queue
    v=q.pops()    remove& return all entries in the queue (least first).
    v=q.pops(i)   remove&return the i least entries in the queue (least first).
    v=q.pops(-i)  remove&return all but the i greatest entries in the queue
                  (least first).
    """
    def __init__(self, data=[]):
        """create a new priority Queue (build heap structure)"""
        self._a = [None] * (1 + len(data))
        for i in range(1, len(self._a)):
            self._bubbleup(i, data[i-1])

    def __len__(self):
        """number of elements currently in the priority queue"""
        return len(self._a)-1

    def top(self):
        """view top item v w/o removing it"""
        return self._a[1]

    def pop(self):
        """pop v from PQ and return it."""
        a = self._a
        result = a[1]
        leaf = self._holetoleaf(1)
        if leaf != len(self):
            a[leaf] = a[-1]
            self._bubbleup(leaf, a[-1])
        self._a = a[:-1]
        return result

    def pops(self, maxRemove=None):
        """pop maxRemove elements from PQ and return a list of results

        If maxRemove < 0, all but maxRemove elements.  If >= 0,
        remove at most maxRemove elements (max len, of course).
        If None, remove all elements.  The result list is "best" first."""
        if maxRemove is None:
            maxRemove = len(self)
        elif maxRemove < 0:
            maxRemove += len(self)
        elif maxRemove > len(self):
            maxRemove = len(self)
        result = [None] * maxRemove
        for i in range(maxRemove):
            result[i] = self.pop()
        return result

    def push(self, v):
        """Add entry v to priority queue"""
        self._a.append(v)
        self._bubbleup(len(self), v)

    def pushes(self, lst):
        """Add all elements in lst to priority queue"""
        pos = len(self)
        self._a += lst
        for leaf in range(pos, len(self._a)):
            self._bubbleup(leaf, self._a[leaf])

    def cream(self, v):
        """Replace top entry in priority queue with v, then return best"""
        if 0 < len(self) and self._a[1] < v:  # comparison with v
            r = self._a[1]
            leaf = self._holetoleaf(1)
            self._bubbleup(leaf, v)
        else:
            r = v
        return r

    def _drop(self, node):
        """drop an entry from PQ."""
        leaf = self._holetoleaf(node)
        if leaf != len(self):
            self._a[leaf] = self._a[-1]
        del self._a[-1]

    def _holetoleaf(self, node):
        """Drive the empty cell at node to the leaf level. Return position"""
        limit = len(self)
        a = self._a
        kid = node * 2
        while kid < limit:
            if not a[kid] < a[kid + 1]:    # comparison
                kid += 1
            a[node] = a[kid]
            node = kid
            kid = node * 2
        if kid == limit:
            a[node] = a[kid]
            return kid
        return node

    def _bubbleup(self, node, v):
        """a[i] is as low as v need be.  Bubble it up."""
        a = self._a
        while node > 1:
            parent = node >> 1
            if not v < a[parent]:          # comparison
                break
            a[node] = a[parent]
            node = parent
        a[node] = v

    def _push(self, v, i):
        """Add entry v to priority queue replacing position i"""
        leaf = self._holetoleaf(i)
        self._bubbleup(leaf, v)

    def __repr__(self):
        return ''.join([self.__class__.__name__, '(', repr(self._a[1:]), ')'])
