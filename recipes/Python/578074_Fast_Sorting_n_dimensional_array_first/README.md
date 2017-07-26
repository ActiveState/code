## Fast Sorting of n dimensional array by first dimension   
Originally published: 2012-03-14 15:14:11  
Last updated: 2012-03-14 15:14:11  
Author: Garrett   
  
I have looked far and wide for code for fast sorting of n dimensional arrays by the first element, for example if I had the array:  
    ray = [[1,2,3,7,5][10,11,12,13,14]] 

I would want it to come out as 
    ray = [[1,2,3,5,7][10,11,12,14,13]]

There are several ways to do this.  One is
    zipped = zip(*ray)
    zipped.sort()
    ray = zip(*zipped)

but this is extremely slow.  Numpy has a much faster way to do it, but it wasn't immediately apparent.

if the above were a numpy array you could simply do the following:
    indexes = numpy.argsort(ray[0])
    for n in xrange(len(ray))
        ray[n] = ray[n][indexes]

I did a time test of the two methods below.