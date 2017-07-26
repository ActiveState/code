import sys
import math 

def is_prime(num):
	for j in range(2,int(math.sqrt(num)+1)):
		if (num % j) == 0: 
			return False
	return True

def main(argv):

	if (len(sys.argv) != 2):
		sys.exit('Usage: prime_numbers4.py <nth_prime>')

	i = 0
	num = 2
	nth = int(sys.argv[1])
		
	while i < nth:
		if is_prime(num): 
			i += 1
			if i == nth:
				print 'The ' + str(nth) + ' prime number is: ' + str(num)
		num += 1 
	
if __name__ == "__main__":
	main(sys.argv[1:])
	
