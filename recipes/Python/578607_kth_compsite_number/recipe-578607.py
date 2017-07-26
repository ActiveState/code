import sys
from collections import deque

def main(argv):

	if len(argv) != 5:
		sys.exit('Usage: kth.py <a> <b> <c> <k> <echo>')

	# get bases
	a = int(sys.argv[1])
	b = int(sys.argv[2])
	c = int(sys.argv[3])
	k = int(sys.argv[4])
	echo = int(sys.argv[5])
	
	# setup queue
	q1 = deque([])
	q2 = deque([])
	q3 = deque([])

	# init variables
	q1.append(1)
	val = 0

	for i in range(k):
	
		# set v to the next value in queue or to MAX_INT if queue empty
		if len(q1) > 0: v1 = q1[0] 
		else: v1 = 2**32
		
		if len(q2) > 0: v2 = q2[0]
		else: v2 = 2**32
		
		if len(q3) > 0: v3 = q3[0]
		else: v3 = 2**32
		
		# choose the next minimum value from the 3 queues
		val = min(v1,v2,v3)
		
		# add next values to queue
		if val == v1:
			q1.popleft()
			q1.append(a*val)
			q2.append(b*val)
		elif val == v2:
			q2.popleft()
			q2.append(b*val)
		elif val == v3:
			q3.popleft()
		
		# always add the largest
		q3.append(c*val)
		
		# if echo is True print every number
		if echo: print str(i+1) + ": " + str(val)
	
	print '\nThe kth number is: ' + str(val) + '\n'
	
if __name__ == "__main__":
	main(sys.argv[1:])
