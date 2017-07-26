#! /usr/bin/env python3

from inspect import getsource
from functools import wraps

# get the globals out of the way
a, b, c = 0, 1, 2

def runtime(f):
	"""Evaluates the given function each time it is called."""
	# get the function's name
	name = f.__name__
	# and its source code, sans decorator
	source = remove_decorators(getsource(f))
	@wraps(f)
	def wrapped(*args, **kwargs):
		# execute the function's declaration
		exec(source)
		# since the above overwrites its name in the local
		# scope we can call it here using eval
		return eval("%s(*%s, **%s)" % (name, args, kwargs))
	return wrapped

def remove_decorators(source):
	"""Removes the decorators from the given function"""
	lines = source.splitlines()
	new_source = '\n'.join((line for line in lines if not line.startswith('@')))
	return new_source

@runtime
def example1(x, y=[]):
	y.append(x)
	return y

@runtime
def example2(x=a**2+2*b+c):
	return x

if __name__ == "__main__":
	print("Testing example1")
	print(example1(1))
	print(example1(2))
	print(example1(3))
	print()
	print("Testing example2 with default values")
	print(example2())
	print("Changing a to 5")
	a = 5
	print(example2())
