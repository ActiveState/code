# PRNG (Pseudo-Random Number Generator) Test
# PRNG info:
# http://en.wikipedia.org/wiki/Pseudorandom_number_generator
# FB - 201012046
# Compares output distribution of any given PRNG
# w/ an hypothetical True-Random Number Generator (TRNG)
import math
import time
global x
x = time.clock() # seed for the PRNG

# PRNG to test
def prng():
    global x
    x = math.fmod((x + math.pi) ** 2.0, 1.0)
    return x

# combination by recursive method
def c(n, k):
    if k == 0: return 1
    if n == 0: return 0
    return c(n - 1, k - 1) + c(n - 1, k)

### combination by multiplicative method
##def c_(n, k):
##    mul = 1.0
##    for i in range(k):
##        mul = mul * (n - k + i + 1) / (i + 1)
##    return mul

# MAIN
n = 20 # number of bits in each trial
print 'Test in progress...'
print
cnk = [] # array to hold bit counts
for k in range(n + 1):
    cnk.append(0)

# generate 2**n n-bit pseudo-random numbers
for j in range(2 ** n):
    # generate n-bit pseudo-random number and count the 0's in it
    # num = ''
    ctr = 0
    for i in range(n):
        b = int(round(prng())) # generate 1 pseudo-random bit
        # num += str(b)
        if b == 0: ctr += 1
    # print num
    # increase bit count in the array
    cnk[ctr] += 1

print 'Number of bits in each pseudo-random number (n) =', n
print
print 'Comparison of "0" count distributions:'
print
print ' k', '    c(n,k)', '    actual', '%dif'
difSum = 0
for k in range(n + 1):
    cnk_ = c(n, k)
    dif = abs(cnk_ - cnk[k])
    print '%2d %10d %10d %4d' % (k, cnk_, cnk[k], 100 * dif / cnk_)
    difSum += dif
print
print 'Difference percentage between the distributions:'
print 100 * difSum / (2 ** n)
