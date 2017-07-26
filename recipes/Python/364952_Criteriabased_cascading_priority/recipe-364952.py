from Queue import Queue
from sets import Set

class PriorityQueue:
    """Simple criteria-based priority queue. Not thread-safe.
    
    The criteria argument should be a sequence of callables that return
    boolean values. There is no need to add an "all pass" criterion at the
    end; the queue will add all non-matching items with the least priority.
    
    The items are retrieved highest-rank first."""
    def __init__(self, criteria):
        self.qs = [Queue(0) for i in range(len(criteria)+1)]
        self.cr = criteria
    def empty(self):
        for q in self.qs:
            if not q.empty():
                return False
        return True
    def put(self, item):
        for i, c in enumerate(self.cr):
            if c(item):
                self.qs[i].put(item)
                return
        self.qs[-1].put(item)
    def get(self):
        for q in self.qs:
            if not q.empty():
                return q.get()
