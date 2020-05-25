from __future__ import division 
from math import ceil

N = 101
n = range(N)
n[::3]=['Fizz']*int(ceil(N/3))
n[::5]= [ t + "Buzz" if type(t) == str else "Buzz" for t in n[::5] ] 

print '\n'.join(str(n) for n in n[1:])
