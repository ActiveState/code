## weighted choice (short and easy numpy version)Originally published: 2006-10-31 12:09:20 
Last updated: 2006-10-31 12:09:20 
Author: James Coughlan 
 
Just a few lines of code if you are willing to use numpy. Uses fact that any prob. distr. can be sampled by computing the cumulative distribution, drawing a random number from 0 to 1, and finding the x-value where that number is attained on the cumulative distribution. The searchsorted(..) function performs this search.