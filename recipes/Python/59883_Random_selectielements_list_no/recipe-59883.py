from random import *

data = range(10000)

# the original, naive version
def select(data):
	if data != []:
		elem = choice(data)
		data.remove(elem)
		return elem
	else:
		return None


# "final" version 
def select(data):
	if data != []:
		pos = randrange( len(data) )
		elem = data[pos]
		data[pos] = data[-1]
		del data[-1]
		return elem
	else:
		return None
