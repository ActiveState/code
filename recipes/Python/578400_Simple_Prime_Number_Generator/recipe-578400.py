import sys

def is_prime(num):
	for j in range(2,num):
		if (num % j) == 0: 
			return False
	return True

def main(argv):

	if (len(sys.argv) != 3):
		sys.exit('Usage: prime_numbers1.py <lowest_bound> <upper_bound>')

	low = int(sys.argv[1])
	high = int(sys.argv[2])
	

		
	for i in range(low,high,1):
		if is_prime(i): 
			print i,
		
if __name__ == "__main__":
	main(sys.argv[1:])
	
