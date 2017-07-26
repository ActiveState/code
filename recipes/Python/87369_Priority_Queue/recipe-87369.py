import Queue

class PriorityQueue(Queue.Queue):
    def _put(self, item):
        data, priority = item
        self._insort_right((priority, data))
        
    def _get(self):
        return self.queue.pop(0)[1]

    def _insort_right(self, x):
        """Insert item x in list, and keep it sorted assuming a is sorted.
        
        If x is already in list, insert it to the right of the rightmost x.       
        """
        a = self.queue
        lo = 0        
        hi = len(a)
        
        while lo < hi:
            mid = (lo+hi)/2
            if x[0] < a[mid][0]: hi = mid
            else: lo = mid+1
        a.insert(lo, x)

def test():
    pq = PriorityQueue()

    pq.put(('b', 1))
    pq.put(('a', 1))
    pq.put(('c', 1))
    pq.put(('z', 0))
    pq.put(('d', 2))

    while not pq.empty():
        print pq.get(),   
    
test() # prints z b a c d
