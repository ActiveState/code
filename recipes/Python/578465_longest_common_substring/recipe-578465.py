#!/usr/bin/env python3.2

import numpy as np

def longest_common_substring(src, dst) :
	c = np.zeros((len(src), len(dst)), dtype=np.int)
	z = 0
	src_m = None
	dst_m = None
	for i in range(len(src)) :
		for j in range(len(dst)) :
			if src[i] == dst[j] :
				if i == 0 or j == 0 :
					c[i,j] = 1
				else :
					c[i, j] = c[i-1, j-1] + 1
				if c[i, j] > z :
					z = c[i, j]
				if c[i, j] == z :
					src_m = (i-z+1, i+1)
					dst_m = (j-z+1, j+1)
			else :
				c[i, j] = 0
	return src_m, dst_m
	
>>> a = """Lorem ipsum dolor sit amet consectetur adipiscing
	elit Ut id nisl quis lacus lobortis egestas id nec turpis""".split()
>>> b = """Lorem ipsum lobortis dolor sit adipiscing elit dolor
	amet consectetur Ut id nisl quis lacus egestas id nec turpis""".split()
>>> src_m, dst_m = longest_common_substring(a, b)
>>> print(src_m[0], src_m[1])
8 13
>>> print(a[src_m[0]:src_m[1]])
['Ut', 'id', 'nisl', 'quis', 'lacus']
>>> print(dst_m[0], dst_m[1])
10 15
>>> print(b[dst_m[0]:dst_m[1]])
['Ut', 'id', 'nisl', 'quis', 'lacus']
