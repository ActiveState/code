from __future__ import division 
from math import ceil

N = 101
n = map(str, range(N))
n[::3]=['Fizz']*int(ceil(N/3))
n[::5]=['Buzz']*int(ceil(N/5))
n[::15]=['FizzBuzz']*int(ceil(N/15))

print '\n'.join(str(n) for n in n[1:])
