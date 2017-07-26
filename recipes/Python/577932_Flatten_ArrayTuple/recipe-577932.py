flatten = lambda arr: reduce(lambda x, y: ((isinstance(y, (list, tuple)) or x.append(y)) and x.extend(flatten(y))) or x, arr, [])

def flatten(array):
	"""
		Returns a list o flatten elements of every inner lists (or tuples)
		****RECURSIVE****
	"""
	res = []
	for el in array:
		if isinstance(el, (list, tuple)):
			res.extend(flatten(el))
			continue
		res.append(el)
	return res


>>> a = [0, 10, 20, [30, (40, 50, [60, [70, [80]], {'hello': 'world'}]), 90], set(['world', 'hello'])]
>>> flatten(a)
[0, 10, 20, 30, 40, 50, 60, 70, 80, {'hello': 'world'}, 90, set(['world', 'hello'])]
