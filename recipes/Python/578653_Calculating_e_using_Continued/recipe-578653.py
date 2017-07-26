# Calculating e using Continued Fraction
# http://en.wikipedia.org/wiki/Continued_fraction
import math
n = 18 # number of iterations
x = 0.0
for i in range(n, 0, -1):

    if i % 3 == 1:
        j = int(i / 3) * 2
    else:
        j = 1

    x = 1.0 / (x + j)

print x + 1, math.e
