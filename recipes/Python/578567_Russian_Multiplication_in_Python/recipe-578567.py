import sys

def main(argv):

	if len(argv) != 2:
		sys.exit('Usage: russian_multi.py <a> <b>')
		
	a = int(sys.argv[1])
	b = int(sys.argv[2])
	
	sum = 0;

	if a == 0 or b == 0:
		print 0;
		exit();

	if b%2 == 1:
		sum += a;

	while b != 1:
		a = a*2;
		b = b/2;
		if b%2 == 1:
			sum += a;
		
	print "The result of " + str(a) + " times " + str(b) + " is: " + str(sum)

if __name__ == "__main__":
	main(sys.argv[1:])
