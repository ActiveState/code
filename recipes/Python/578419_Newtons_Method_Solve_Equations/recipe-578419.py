import sys

def f(x):
	return x**3 + x - 1
	
def f_prime(x):
	return 3*x**2 + 1

def newt(x,n):
	for i in range(n):
		if f_prime(x) == 0:
			return x
		x = x - f(x)/f_prime(x)
	return x
	
def main(argv):
	if (len(sys.argv) != 3):
		sys.exit('Usage: newtons_method.py <x> <n>')
	
	print 'The root is: ',
	print newt(float(sys.argv[1]),int(sys.argv[2]))

if __name__ == "__main__":
	main(sys.argv[1:])
