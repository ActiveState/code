import sys

def main(argv):

	if len(argv) != 2:
		sys.exit('Usage: simple_multi.py <a> <b>')
		
	a = int(sys.argv[1])
	b = int(sys.argv[2])
	sum = 0
	
	for i in range(a):
		sum += b
		
	print "The result of " + str(a) + " times " + str(b) + " is: " + str(sum)

if __name__ == "__main__":
	main(sys.argv[1:])
