import sys

def is_prime(num):
	for j in range(2,num):
		if (num % j) == 0: 
			return False
	return True

def main(argv):

	if (len(sys.argv) != 3):
		sys.exit('Usage: prime_numbers2.py <lowest_bound> <upper_bound>')

	low = int(sys.argv[1])
	high = int(sys.argv[2])
	
	if (low == 2):
		print 2, 
	
	if (low % 2 == 0):
		low += 1
		
	for i in range(low,high,2):
		if is_prime(i): 
			print i, 
		
if __name__ == "__main__":
	main(sys.argv[1:])
