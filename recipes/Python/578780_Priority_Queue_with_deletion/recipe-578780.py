import heapq

class PriorityQueue(dict):
    def __init__(self, _, f):
        self.f = f
        self.heap = []
    
    def __delitem__(self, item):
        self._remove_from_dict(item)
        self.heap = [(v,k) for v,k in self.heap if k != item]
        heapq.heapify(self.heap)
    
    def pop(self):
        _, smallest = heapq.heappop(self.heap)
        self._remove_from_dict(smallest)
        return smallest

    def append(self, item):
        self[item]=item
        heapq.heappush(self.heap, (self.f(item), item))

    def _remove_from_dict(self, item):
        super(PriorityQueue, self).__delitem__(item)
