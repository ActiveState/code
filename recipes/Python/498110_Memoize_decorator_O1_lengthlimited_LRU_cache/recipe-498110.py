import cPickle

__all__ = ['memoize']


# This would usually be defined elsewhere
class decoratorargs(object):
	def __new__(typ, *attr_args, **attr_kwargs):
		def decorator(orig_func):
			self = object.__new__(typ)
			self.__init__(orig_func, *attr_args, **attr_kwargs)
			return self
		
		return decorator


class memoize(decoratorargs):
	class Node:
		__slots__ = ['key', 'value', 'older', 'newer']
		def __init__(self, key, value, older=None, newer=None):
			self.key = key
			self.value = value
			self.older = older
			self.newer = newer
	
	def __init__(self, func, capacity, keyfunc=lambda *args, **kwargs: cPickle.dumps((args, kwargs))):
		self.func = func
		self.capacity = capacity
		self.keyfunc = keyfunc
		self.reset()
	
	def reset(self):
		self.mru = self.Node(None, None)
		self.mru.older = self.mru.newer = self.mru
		self.nodes = {self.mru.key: self.mru}
		self.count = 1
		self.hits = 0
		self.misses = 0
	
	def __call__(self, *args, **kwargs):
		key = self.keyfunc(*args, **kwargs)
		try:
			node = self.nodes[key]
		except KeyError:
			# We have an entry not in the cache
			self.misses += 1
			
			value = self.func(*args, **kwargs)

			lru = self.mru.newer  # Always true
			
			# If we haven't reached capacity
			if self.count < self.capacity:
				# Put it between the MRU and LRU - it'll be the new MRU
				node = self.Node(key, value, self.mru, lru)
				self.mru.newer = node
	
				lru.older = node
				self.mru = node
				self.count += 1
			else:
				# It's FULL! We'll make the LRU be the new MRU, but replace its
				# value first
				del self.nodes[lru.key]  # This mapping is now invalid
				lru.key = key
				lru.value = value
				self.mru = lru

			# Add the new mapping
			self.nodes[key] = self.mru
			return value
		
		# We have an entry in the cache
		self.hits += 1
		
		# If it's already the MRU, do nothing
		if node is self.mru:
			return node.value
		
		lru = self.mru.newer  # Always true
		
		# If it's the LRU, update the MRU to be it
		if node is lru:
			self.mru = lru
			return node.value
		
		# Remove the node from the list
		node.older.newer = node.newer
		node.newer.older = node.older
		
		# Put it between MRU and LRU
		node.older = self.mru
		self.mru.newer = node
		
		node.newer = lru
		lru.older = node
		
		self.mru = node
		return node.value


# Example usage - fib only needs a cache size of 3 to keep it from
# being an exponential-time algorithm
@memoize(3)
def fib(n): return (n > 1) and (fib(n - 1) + fib(n - 2)) or 1

fib(100)  # => 573147844013817084101L

# This is faster because it doesn't use the default key function -
# it doesn't need to call cPickle.dumps((*args, **kwargs))
@memoize(100, lambda n: n)
def fib(n): return (n > 1) and (fib(n - 1) + fib(n - 2)) or 1

fib(100)  # => 573147844013817084101L

# See what's in the cache
# => [(98, 218922995834555169026L), (99, 354224848179261915075L), (100, 573147844013817084101L)]
[(node.key, node.value) for node in fib.nodes.values()]

# Get an example of the key function working
fib.keyfunc(40)  # => 40

# Simple report on performance
# => Hit %: 0.492462
print 'Hit %%: %f' % (float(fib.hits) / (fib.hits + fib.misses))

# Resize the LRU cache
fib.capacity = 100
fib.reset()  # Not necessary unless you shrink it
