###Generator for integer partitions

Originally published: 2003-08-27 14:02:53
Last updated: 2003-08-27 14:02:53
Author: David Eppstein

A "partition" is a way of representing a given integer as a sum of zero or more positive integers, e.g. the partitions of 4 are 1+1+1+1, 1+1+2, 2+2, 1+3, and 4.  This recipe uses simple generators recursively to produce a stream of all partitions of its argument.  Each partition is represented as a sorted list of the numbers to be summed, e.g. [1,1,1,1], [1,1,2], [2,2], [1,3], [4].