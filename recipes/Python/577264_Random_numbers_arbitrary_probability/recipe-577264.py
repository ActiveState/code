# Generating N random numbers that probability distribution
# fits to any given function curve
# FB - 201006137

import math
import random

# define any function here!
def f(x):
    return math.sin(x)
# f(x) = 1.0 : for uniform probability distribution

# f(x) = x : for triangular probability distribution
# (math.sqrt(random.random()) would also produce triangular p.d. though.)

# f(x) = math.exp(-x*x/2.0)/math.sqrt(2.0*math.pi) : for std normal p.d.
# (taking average of (last) 2,3,... random.random() values would also
# produce normal probability distributions though.)

# define any xmin-xmax interval here! (xmin < xmax)
xmin = 0.0
xmax = math.pi

# find ymin-ymax
numSteps = 1000000 # bigger the better but slower!
ymin = f(xmin)
ymax = ymin
for i in range(numSteps):
    x = xmin + (xmax - xmin) * float(i) / numSteps
    y = f(x)
    if y < ymin: ymin = y
    if y > ymax: ymax = y

n = 10 # how many random numbers to generate
for i in range(n):
    while True:
        # generate a random number between 0 to 1
        xr = random.random()
        yr = random.random()
        x = xmin + (xmax - xmin) * xr
        y = ymin + (ymax - ymin) * yr
        if y <= f(x):
            print xr
            break
