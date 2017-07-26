# Check if the function already exists first
try:
	enumerate
except:	
	# Allow access like a builtin function
	import __builtin__
	__builtin__.enumerate = lambda seq: zip(xrange(len(seq)), seq)
