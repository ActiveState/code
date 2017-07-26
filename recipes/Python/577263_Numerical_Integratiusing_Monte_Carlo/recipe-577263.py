# Numerical Integration using Monte Carlo method
# FB - 201006137
import math
import random

# define any function here!
def f(x):
    return math.sin(x)

# define any xmin-xmax interval here! (xmin < xmax)
xmin = 0.0
xmax = 2.0 * math.pi

# find ymin-ymax
numSteps = 1000000 # bigger the better but slower!
ymin = f(xmin)
ymax = ymin
for i in range(numSteps):
    x = xmin + (xmax - xmin) * float(i) / numSteps
    y = f(x)
    if y < ymin: ymin = y
    if y > ymax: ymax = y

# Monte Carlo
rectArea = (xmax - xmin) * (ymax - ymin)
numPoints = 1000000 # bigger the better but slower!
ctr = 0
for j in range(numPoints):
    x = xmin + (xmax - xmin) * random.random()
    y = ymin + (ymax - ymin) * random.random()
    if math.fabs(y) <= math.fabs(f(x)):
    if f(x) > 0 and y > 0 and y <= f(x):
        ctr += 1 # area over x-axis is positive
    if f(x) < 0 and y < 0 and y >= f(x):
        ctr -= 1 # area under x-axis is negative

fnArea = rectArea * float(ctr) / numPoints
print "Numerical integration = " + str(fnArea)
