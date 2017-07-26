import sys
import math 
import random

def is_prime(num):
	for j in range(2,int(math.sqrt(num)+1)):
		if (num % j) == 0: 
			return False
	return True

def main(argv):

	if (len(sys.argv) != 2):
		sys.exit('Usage: prime_numbers6.py <num_digits>')


	digits = int(sys.argv[1])
	low = int('1' + '0' * (digits-1))
	high = int('9' * digits)
	done = False	
			
	if (low == 1):
		low = 2
			
	while not done:
		num = random.randint(low,high)
		if is_prime(num): 
			print 'A random ' + str(digits) + ' prime number is: ' + str(num)
			done = True
			
	
		
if __name__ == "__main__":
	main(sys.argv[1:])
