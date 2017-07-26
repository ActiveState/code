## Safe heap queue class

Originally published: 2005-10-08 09:30:19
Last updated: 2005-10-09 14:57:08
Author: George Sakkis

The Heap class is an improvement over a previous recipe (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/437116) that also wraps the heapq module. There are two main differences from the other recipe:\n- All methods on this heap preserve the heap property invariant; therefore there is no need for is_heap().\n- When creating a new heap, an optional 'key' argument can be specified to determine the comparison key for the items to be pushed into the heap.