import sys

def main(argv):

	if len(argv) != 2:
		sys.exit('Usage: simple_multi.py <a> <b>')
		
	a = int(sys.argv[1])
	b = int(sys.argv[2])
		
	print "The result of " + str(a) + " times " + str(b) + " is: " + str(a*b)

if __name__ == "__main__":
	main(sys.argv[1:])
