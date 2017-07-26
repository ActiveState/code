## Python Octree Implementation 
Originally published: 2006-09-21 03:12:00 
Last updated: 2006-09-21 03:12:00 
Author: Ben Harling 
 
This is a simple implementation of an octree data structure in python. Its use is primarily for fast collision or view frustrum culling in interactive 3d environments, but its possible uses are quite open-ended. It was originally written for use with the pyOgre 3d engine binding. The code makes use of recursive functions to insert and find nodes in the octree, and is heavily commented. It can store any type of object you create, so long as that object has a 'position' property in the form of a 3-vector tuple. It includes a test function which relies on the random module, but the octree itself has no required dependencies. It will try to use the psyco module to speed up its execution, but that is not essential.