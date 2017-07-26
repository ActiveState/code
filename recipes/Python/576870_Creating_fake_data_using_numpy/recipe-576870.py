from numpy.random import normal
from scipy.stats import norm as normStat


CRAZINESS = 0.1
MIN = 50 
MAX = 300
STEP = 5
AVG = 180
DEV = 40 
p = normStat(AVG, DEV).pdf

def noise():
    return 1 + CRAZINESS * normal(1)

for x in range(MIN, MAX, STEP):
    print str(x), "\t",   p(x) * noise()
