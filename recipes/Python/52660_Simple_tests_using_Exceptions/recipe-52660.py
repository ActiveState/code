def IsInt( str ):
	""" Is the given string an integer?	"""
	ok = 1
	try:
		num = int(str)
	except ValueError:
		ok = 0
	return ok

def IsAllDigits( str ):
	""" Is the given string composed entirely of digits? """
	import string
	match = string.digits
	ok = 1
	for letter in str:
		if letter not in match:
			ok = 0
			break
	return ok

if __name__ == '__main__':
	print IsInt('23')
	print IsInt('sd')
	print IsInt('233835859285')
	print IsAllDigits('233835859285')
