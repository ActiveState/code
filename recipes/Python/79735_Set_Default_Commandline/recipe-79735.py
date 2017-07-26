import sys

def isint(x):
	try:
		x = int(x)
		return 1
	except:
		return 0

def isarg(pos):
	try:
		temp = sys.argv[pos]
		temp = 1
	except:
		temp = 0
	return temp

def setarg(pos, val):
	if isarg(pos):
		if isint(sys.argv[pos]):
			return int(sys.argv[pos])
		else:
			return sys.argv[pos]
	else:

		sys.argv.append(str(val)) # str(val) is used, because by default all arguments are strings  
		if isint(sys.argv[len(sys.argv)-1]):
			return int(sys.argv[len(sys.argv)-1])
		else:
			return sys.argv[len(sys.argv)-1]

## usage : FileNameToProcess = setarg(1, "default.txt")

## Explanation:
##     if there is an argument at sys.argv[1], return that value;
##     if not, sys.argv[1] to "default.txt"
