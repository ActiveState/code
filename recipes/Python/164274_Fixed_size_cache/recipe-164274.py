import weakref

class DoubleNode:
    """node for a double linked list """ 
    previous = None
    next = None
    def __init__(self, value):
	self.value = value
    def extract(self):
	previous = self.previous
	next = self.next
	if previous:
	    previous.next = next
	if next:
	    next.previous = previous
	self.next = self.previous = None
    def insert_after(self, node):
	self.next = node.next
	self.previous = node
	node.next.previous = self
	node.next = self

class BufferCache:
    """Store data in a double linked list..."""
    count = 0
    def __init__(self, function, capacity=50):
	self.cache = weakref.WeakValueDictionary()
	self.next = self.previous = self
	self.function = function
	self.capacity = capacity

    def _append(self, value):
	""" append a node for a new value """ 
	node = DoubleNode(value)
	node.insert_after(self.previous)
	if self.count == self.capacity:
	    self.next.extract()
	else:
	    self.count += 1
	return node
    def _value(self, node):
	"""return the value and put the node as the first one"""
	node.extract()
	node.insert_after(self.previous)
	return node.value
    
    def __call__(self, *args):
	try:
	    node = self.cache[args]
	except KeyError:
	    x = self.function(*args)
	    self.cache[args] = self._append(x)
	else:
	    x = self._value(node)
	return x
	    
    def __repr__(self):
	i = self.previous
	s = "" 
	while i!=self:
	    s = s + repr(i.value) + " " 
	    i = i.previous	    
	return s

#
# sample
#
def foo(x):
    print "computing"
    return "*" + str(x)

foo_cache = BufferCache(foo,5)
for i in range(5):
    print foo_cache(i)
print foo_cache(2)
