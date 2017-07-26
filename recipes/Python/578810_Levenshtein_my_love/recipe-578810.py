#!/usr/bin/env python3

def square_list(a, b, value=0) :
	return [[value,] * b for j in range(a)]

def arg_min(* arg_list) :
	arg_s = None
	for i, arg in enumerate(arg_list) :
		if i == 0 or arg < arg_s :
			arg_s = arg
			i_s = i
	return i_s, arg_s

MODIFIED = 0
DELETED = 1
CREATED = 2

def levenshtein_distance(a, b) :
	""" return the levenshtein distance between two strings of list of """

	len_a = len(a)
	len_b = len(b)
	
	d = square_list(len_a+1, len_b+1)
	
	for i in range(1, len_a+1) :
		d[i][0] = i
	for j in range(1, len_b+1) :
		d[0][j] = j
		
	for j in range(1, len_b+1) :
		for i in range(1, len_a+1) :
			if a[i-1] == b[j-1] :
				d[i][j] = d[i-1][j-1]
			else :
				d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
	return d[-1][-1]

def levenshtein_sequence(a, b) :
	""" return an explicit list of difference between a and b """

	len_a = len(a)
	len_b = len(b)
	
	s = list()
	
	d = square_list(len_a+1, len_b+1)
	
	for i in range(1, len_a+1) :
		d[i][0] = i
	for j in range(1, len_b+1) :
		d[0][j] = j
	
	for j in range(1, len_b+1) :
		for i in range(1, len_a+1) :
			if a[i-1] == b[j-1] :
				d[i][j] = d[i-1][j-1]
			else :
				d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
				
	prev_i, prev_j = i, j
	while i > 0 and j > 0 :
		if i == 1 and j == 1 :
			if prev_i != i and prev_j != j :
				u = MODIFIED
			elif prev_i == i :
				u = CREATED
			elif prev_j == j :
				u = DELETED
			new_i, new_j = i-1, j-1
		elif i == 1 :
			new_i, new_j = i, j-1
			u = CREATED
		elif j == 1 :
			u = DELETED
			new_i, new_j = i-1, j
		else :
			u, null = arg_min(d[i-1][j-1], d[i-1][j], d[i][j-1])
			new_i, new_j = i - (1,1,0)[u], j - (1,0,1)[u]
		op = '*-+'[u] if d[i][j] != d[new_i][new_j] else '='
		s.append((op, i-1, j-1))
		prev_i, prev_j = i, j
		i, j = new_i, new_j
		
	return list(reversed(s))
