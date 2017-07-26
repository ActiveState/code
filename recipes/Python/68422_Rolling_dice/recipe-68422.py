def dice( num, sides ):
	return reduce(lambda x, y, s = sides: x + random.randrange(s), range( num + 1 )) + num
