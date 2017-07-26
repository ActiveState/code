import random

def windex(lst):
	'''an attempt to make a random.choose() function that makes weighted choices
	
	accepts a list of tuples with the item and probability as a pair
	like: >>> x = [('one', 0.25), ('two', 0.25), ('three', 0.5)]
	>>> y=windex(x)'''
	n = random.uniform(0, 1)
	for item, weight in lst:
		if n < weight:
			break
		n = n - weight
	return item
