###sorting part2 -- some performance considerations

Originally published: 2004-09-24 11:20:33
Last updated: 2004-09-24 21:48:22
Author: John Nielsen

Below you will find a simple python class that I wrote to test performance of\nvarious different sorting techniques. In this cas: list, heapq, and bisect. For printing out data, I make use of the very cool decimal module to limit errant floating point numbers with many digits. It helps me decide when I want to think about different types of sorts.\n\nPython's list.sort is so good that generally you are not going to want to write\nyour own sort, and instead use it and some of the new features recently added to it.  However, with a list.sort you pay for sorting at retrieval time.  A different type of sort using data structures to sort at creation time instead of retrieval can offer some performance characteristics, that may make one consider them instead.