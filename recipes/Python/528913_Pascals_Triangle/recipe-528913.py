#! /usr/bin/env python

"""
For a given number, prints Pascal's Triangle upside-down up to that line.

Takes advantage of the fact that the Triangle is symmetric.
Uses the combinatorics property of the Triangle: 
	For any NUMBER in position INDEX at row ROW:
	NUMBER = C(ROW, INDEX)

A hash map stores the values of the combinatorics already calculated, so
the recursive function speeds up a little.

Prints everything alligned at first, but starts screwing up at about 13.


tn.pablo@gmail.com
03/09/07
"""

import sys

def comb(N, n, combs):
	""" 
	Returns the value of C(N,n). 
	First the function looks it up in a dictionary and only calculates
	if it isn't present, in which case it works recursively.
	"""
	try:
		ans = combs[(N,n)]
	except KeyError:
		if n == 0: ans=1
		elif n == 1: ans=N
		else:
			ans = (comb(N, n-1, combs) * (N-n+1) * 1/n)
			combs[(N,n)] = ans
	return ans
	

lines = int(sys.argv[1])
# stack that will contain the items of the row to be mirrored
mirror = []
# dictionary of combinatoric-value pairs
combs = {}
for row in range(lines, -1, -1):
	# insert indentation
	print '    ' * (lines - row),
	# first half of the row
	limit = (row//2)+1
	for index in range(limit):
		num = comb(row, index, combs)
		if not((row%2 == 0) and (index == limit-1)): mirror.append(num)
		print '%i      ' % num,
	# for the second half, mirror the first
	while mirror: print '%i      ' % mirror.pop(),
	print
