## Select the nth smallest elementOriginally published: 2004-02-17 02:14:00 
Last updated: 2004-03-05 08:51:37 
Author: Raymond Hettinger 
 
O(n) quicksort style algorithm for looking up data based on rank order.    Useful for finding medians, percentiles, quartiles, and deciles.  Equivalent to data[n] when the data is already sorted.