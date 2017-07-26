## Priority dictionary

Originally published: 2002-03-08 22:09:16
Last updated: 2002-03-08 22:09:16
Author: David Eppstein

This data structure acts almost like a dictionary, with two modifications: First, D.smallest() returns the value x minimizing D[x].  For this to work correctly, all values D[x] stored in the dictionary must be comparable. Second, iterating "for x in D" finds and removes the items from D in sorted order. Each item is not removed until the next item is requested, so D[x] will still return a useful value until the next iteration of the for-loop.