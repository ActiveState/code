import sys

def main(argv):

	if len(argv) != 2:
		sys.exit('Usage: tens_multi.py <a> <b>')
		
	a = sys.argv[1]
	b = sys.argv[2]
	sum = 0; 
	c = len(a) - 1;

	for i in a:
		d = len(b) - 1;
		for j in b:
			sum += int(i)*int(j)*(10**c)*(10**d); 
			d -= 1; 
		c -= 1;

	print "The result of " + a + " times " + b + " is: " + str(sum)

if __name__ == "__main__":
	main(sys.argv[1:])
