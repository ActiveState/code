## Running median, mean and modeOriginally published: 2013-03-06 17:33:31 
Last updated: 2013-03-06 17:33:32 
Author: Virgil Stokes 
 
The following is a small contribution that I hope can be useful to Python programmers for the calculation of the running median, mean and mode. It is important to note that all the "running" calculations are done for full windows. Here is a simple example:\n\ny = [1, 2, 3, 3, 1, 4], with a sliding window of size = 3 for the running estimations,\nmeans = 2, 2.6667, 2.3333, 2.6667\nmedians = 2, 3, 3, 3\nmodes = 1, 3, 3, 1