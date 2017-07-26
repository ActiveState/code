import sys
import math

def main(argv):

	if len(argv) != 1:
		sys.exit('Usage: calc_pi.py <n>')

	print '\nComputing Pi v.01\n'
	
	a = 1.0
	b = 1.0/math.sqrt(2)
	t = 1.0/4.0
	p = 1.0
		
	for i in range(int(sys.argv[1])):
		at = (a+b)/2
		bt = math.sqrt(a*b)
		tt = t - p*(a-at)**2
		pt = 2*p
		
		a = at;b = bt;t = tt;p = pt
		
	my_pi = (a+b)**2/(4*t)
	accuracy = 100*(math.pi-my_pi)/my_pi
		
	print "Pi is approximately: " + str(my_pi)
	print "Accuracy with math.pi: " + str(accuracy)
	
if __name__ == "__main__":
	main(sys.argv[1:])
		
