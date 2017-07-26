## Heap-based priority queueOriginally published: 2001-10-14 17:04:26 
Last updated: 2001-10-14 17:04:26 
Author: Scott David Daniels 
 
This is a Priority Queue based on a heap data strucuture.  Elements come out of the queue least first.  The heap is a complete binary tree with root at _a[1] and, for a node N, its parent is _a[N>>1] and children are _a[2*N] and _a[2*N+1].