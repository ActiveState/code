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
		sys.exit('Usage: prime_numbers5.py <num_digits>')


	digits = int(sys.argv[1])
	low = int('1' + '0' * (digits-1))
	high = int('9' * digits)
	prime_number_list = []
	
	if (low == 1):
		prime_number_list.append(2)
		low = 3
		
	if (low % 2 == 0):
		low += 1
			
	for i in range(low,high,2):
		if is_prime(i): 
			prime_number_list.append(i)
			
	print 'A random ' + str(digits) + ' prime number is: ' + str(random.choice(prime_number_list))
		
if __name__ == "__main__":
	main(sys.argv[1:])
