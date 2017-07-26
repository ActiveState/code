#! /usr/bin/env python3

"""
runtime.py

Written by Geremy Condra

Licensed under GPLv3

Released 14 May 2009

This module provides a simple decorator used
to reevaluate function arguments at runtime
based on their annotations.
"""

from inspect import getfile, getfullargspec
from functools import wraps

def runtime(f):
	"""Evaluates a function's annotations at runtime.

	Usage:
		>>> @runtime
		... def f(x, y:'[]'):
		... 	y.append(x)
		... 	return y
		...
		>>> f(1)
		[1]
		>>> f(2)
		[2]

	Arguments evaluated at runtime must be treated as
	though they were keyword-only arguments for the
	purposes of assignment.

	Good:
		>>> f(4, y=[1, 2, 3])
		[1, 2, 3, 4]

	Bad:
		>>> f(4, [1, 2, 3])
		TypeError: f() got multiple values for keyword argument 'y'

	For this reason you should always make the arguments
	you want evaluated at runtime the last non-keyword
	arguments to your function.

	If you need a varargs argument, just place your
	runtime-evaluated arguments afterwards.

	Good:
		>>> @runtime
		... def f(*args, z:'[]'):
		... 	z.extend(args)
		... 	return z
		...
		>>> f(1, 2, 3, 4)
		[1, 2, 3, 4]
		>>> f(4, 5, 6, 7, z=[1, 2, 3])
		[1, 2, 3, 4, 5, 6, 7]

	Bad:
		>>> @runtime
		... def f(z:'[]', *args):
		... 	z.extend(args)
		... 	return z
		...
		>>> f(1, 2, 3, 4)
		TypeError: f() got multiple values for keyword argument 'z'
	"""

	# get the functions' file of origin
	filename = getfile(f)

	# build the evaluatable annotations table
	comp = lambda stmt: compile(stmt, filename, 'eval')
	defaults = {k: comp(v) for k, v in getfullargspec(f)[-1].items()}

	# build the wrapping function
	@wraps(f)
	def wrapped(*args, **kwargs):
		# update kwargs with the unfilled defaults, evaluated at runtime
		for k, v in defaults.items():
			if k not in kwargs:
				kwargs[k] = eval(v)
		return f(*args, **kwargs)

	# and return it
	return wrapped

@runtime
def example1(x, y:'[]'):
	y.append(x)
	return y

@runtime
def example2(*, x:'a**2+2*b+c'):
	return x

if __name__ == "__main__":
	print("Testing example1")
	print(example1(1))
	print(example1(2))
	print(example1(3))
	print()
	print("Testing example2 with values 0, 1, 2")
	a, b, c = 0, 1, 2
	print(example2())
	print("Changing a to 5")
	a = 5
	print(example2())
