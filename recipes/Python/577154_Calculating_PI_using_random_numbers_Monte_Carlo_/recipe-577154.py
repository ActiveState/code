# Calculating PI using random numbers (Monte Carlo Method)
# FB - 201003265
import math
import random
maxIt = 1000000 # number of iterations (greater the better)

ctr = 0
for i in range(maxIt):
    if math.pow(random.random(), 2.0) + math.pow(random.random(), 2.0) <= 1.0:
        ctr += 1

print "PI = ", 4.0 * ctr / maxIt
