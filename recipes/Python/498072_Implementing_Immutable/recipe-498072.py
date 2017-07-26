#!/usr/bin/env python

"""A tuctionary, or tuct, is the combination of a tuple with
a dictionary. A tuct has named items, but they cannot be
deleted or rebound, nor new can be added.
"""

class tuct(object):
	"""The tuct class. An immutable dictionary.
	"""
	
	def __init__(self, dict=None, **kwds):
		self.__data = {}
		if dict is not None:
			self.__data.update(dict)
		if len(kwds):
			self.__data.update(kwds)
	
	del __init__
	
	def __repr__(self):
		return repr(self.__data)
	
	def __cmp__(self, dict):
		if isinstance(dict, tuct):
			return cmp(self.__data, dict.__data)
		else:
			return cmp(self.__data, dict)
	
	def __len__(self):
		return len(self.__data)
	
	def __getitem__(self, key):
		return self.__data[key]
	
	def copy(self):
		if self.__class__ is tuct:
			return tuct(self.__data.copy())
		import copy
		__data = self.__data
		try:
			self.__data = {}
			c = copy.copy(self)
		finally:
			self.__data = __data
		c.update(self)
		return c
	def keys(self):
		return self.__data.keys()
	
	def items(self):
		return self.__data.items()
		
	def iteritems(self):
		return self.__data.iteritems()
		
	def iterkeys(self):
		return self.__data.iterkeys()
	
	def itervalues(self):
		return self.__data.itervalues()
	
	def values(self):
		return self.__data.values()
		
	def has_key(self, key):
		return self.__data.has_key(key)
	
	def get(self, key, failobj=None):
		if not self.has_key(key):
			return failobj
		return self[key]
		
	def __contains__(self, key):
		return key in self.__data
	
	@classmethod
	def fromkeys(cls, iterable, value=None):
		d = cls()
		for key in iterable:
			d[key] = value
		return d
