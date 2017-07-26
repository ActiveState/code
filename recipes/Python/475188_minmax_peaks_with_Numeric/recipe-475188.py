from Numeric import *

def peaks(data, step):
	n = len(data) - len(data)%step # ignore tail
	slices = [ data[i:n:step] for i in range(step) ]
	peak_max = reduce(maximum, slices)
	peak_min = reduce(minimum, slices)
	return transpose(array([peak_max, peak_min]))

"""example of use:

>>> x = sin(arrayrange(0, 3.14, 1e-5))
>>> len(x)
314000
>>> peaks(x,10000)
array([[ 0.09982347,  0.        ],
       [ 0.19865953,  0.09983342],
         ...
       [ 0.23924933,  0.14112991],
       [ 0.14112001,  0.04159065]])
"""
