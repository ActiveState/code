## Depth first search generator 
Originally published: 2009-11-03 06:36:16 
Last updated: 2009-11-09 04:46:21 
Author: Paul W. Miller 
 
This is the standard iterative DFS code modified to yield the vertices visited, so you don't have to pass a function into the DFS routine to process them.  Note that this code is not quite complete... you'll need to define the function neighbors (v) based on your graph representation.