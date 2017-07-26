# Numerical Integration using random sampling
# FB - 201006292
import math
import random

# define any function here!
def f(x):
    return math.sin(x)

# define any xmin-xmax interval here! (xmin < xmax)
xmin = 0.0
xmax = math.pi

numPoints = 1000000 # bigger the better but slower!
sumy = 0.0
for j in range(numPoints):
    x = xmin + (xmax - xmin) * random.random()
    sumy += f(x)

numInt = (xmax - xmin) * sumy / numPoints     
print "Numerical integral = " + str(numInt)
