def lace(*lists):
	"""lace: forms a list of tuples by interlacing elements from several lists.
	
	That is i-th tuple contains the i-th element from each of 
	the argument sequences. e.g.: 
	>>> a=[1,2,3,4]; b=[100,101,102,103]; c=['w','x','y','z']	
	>>> d=lace(a,b,c); print d; # yields a single list of nested tuples:
	[(1, 100, 'w'), (2, 101, 'x'), (3, 102, 'y'), (4, 103, 'z')]
	
	* NOTE: Unlike the zip built-in (new to Python 2.0), Short lists are extended 
	with values of None to match the longest list if necessary. With zip(), the 
	returned list is truncated in length to the length of the shortest 
	argument sequence which is not always kosher.
	"""
	return apply(map,(None,)+lists)


x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228]
z = ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']
foo = lace(x, y, z); foo # try this and see!
