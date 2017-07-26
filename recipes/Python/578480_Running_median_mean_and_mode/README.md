## Running median, mean and mode  
Originally published: 2013-03-06 17:33:31  
Last updated: 2013-03-06 17:33:32  
Author: Virgil Stokes  
  
The following is a small contribution that I hope can be useful to Python programmers for the calculation of the running median, mean and mode. It is important to note that all the "running" calculations are done for full windows. Here is a simple example:

y = [1, 2, 3, 3, 1, 4], with a sliding window of size = 3 for the running estimations,
means = 2, 2.6667, 2.3333, 2.6667
medians = 2, 3, 3, 3
modes = 1, 3, 3, 1