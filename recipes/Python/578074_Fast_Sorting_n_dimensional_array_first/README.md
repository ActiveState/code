## Fast Sorting of n dimensional array by first dimension 

Originally published: 2012-03-14 15:14:11
Last updated: 2012-03-14 15:14:11
Author: Garrett 

I have looked far and wide for code for fast sorting of n dimensional arrays by the first element, for example if I had the array:  \n    ray = [[1,2,3,7,5][10,11,12,13,14]] \n\nI would want it to come out as \n    ray = [[1,2,3,5,7][10,11,12,14,13]]\n\nThere are several ways to do this.  One is\n    zipped = zip(*ray)\n    zipped.sort()\n    ray = zip(*zipped)\n\nbut this is extremely slow.  Numpy has a much faster way to do it, but it wasn't immediately apparent.\n\nif the above were a numpy array you could simply do the following:\n    indexes = numpy.argsort(ray[0])\n    for n in xrange(len(ray))\n        ray[n] = ray[n][indexes]\n\nI did a time test of the two methods below.