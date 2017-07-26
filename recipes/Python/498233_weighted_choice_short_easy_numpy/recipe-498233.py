from numpy import *
from numpy.random import random

def toss(c, sh):
    """Return random samples of cumulative vector (1-D numpy array) c
    The samples are placed in an array of shape sh.
    Each element of array returned is an integer from 0 through n-1,
    where n is the length of c."""
    
    y = random(sh) #return array of uniform numbers (from 0 to 1) of shape sh
    x = searchsorted(c,y)

    return x

#sample usage:

p=array((0.1, 0.2, 0.6, 0.1)) #vector of probabilities, normalized to 1
c=cumsum(p) #cumulative probability vector

print toss(c, (10,)) #want 10 samples in 1-D array
