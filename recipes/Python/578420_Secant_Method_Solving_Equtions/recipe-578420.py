import sys

def f(x):
	return x**3+x-1
	
def secant(x0,x1,n):
	for i in range(n):
		if f(x1)-f(x0) == 0:
			return x1
		x_temp = x1 - (f(x1)*(x1-x0)*1.0)/(f(x1)-f(x0))
		x0 = x1
		x1 = x_temp
	return x1
	
def main(argv):
	if (len(sys.argv) != 4):
		sys.exit('Usage: secant_method.py <x0> <x1> <n>')
	
	print 'The root is: ',
	print secant(float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]))

if __name__ == "__main__":
	main(sys.argv[1:])
		
