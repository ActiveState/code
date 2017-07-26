import heapq

class Heap(list) :
	def __init__(self, * pos_arg, ** nam_arg) :
		list.__init__(self, * pos_arg, ** nam_arg)
		
	def pop(self) :
		return heapq.heappop(self)
		
	def push(self, item) :
		heapq.heappush(self, item)
		
	def pushpop(self, item) :
		return heapq.heappushpop(self, item)
		
	def poppush(self, itemp) :
		return heapq.replace(self, item)
	
