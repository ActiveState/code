from functools import wraps
from copy import deepcopy

def fluent(method):
	"""Used to define fluent API class methods"""
	@wraps(method)
	def wrapped(self, *args, **kwargs):
		dupe = deepcopy(self)
		method(dupe, *args, **kwargs)
		return dupe
	return wrapped
