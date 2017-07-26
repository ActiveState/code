from collections import deque
from random import random
from math import log

class Infinity(object):
    'Sentinel object that always compares greater than another object'
    def __cmp__(self, other):
        return 1

def running_median(n, iterable, len=len, min=min, int=int, log=log, random=random):
    'Fast running median with O(lg n) updates where n is the window size'

    maxlevels = int(log(n, 2)) + 1
    bottom_to_top = list(range(maxlevels))
    top_to_bottom = bottom_to_top[::-1]

    VALUE, NEXT, WIDTH = 0, 1, 2                # Components of a node list
    NIL = [Infinity(), [], []]                  # Singleton terminator node
    head = ['HEAD', [NIL] * maxlevels, [1] * maxlevels]
    staircase = [None] * maxlevels

    queue = deque()
    queue_append, queue_popleft = queue.append, queue.popleft
    midpoint = n // 2
    oldnode = None
    for newelem in iterable:
        # staircase: first node on each level where node[NEXT][level][VALUE] > newelem
        queue_append(newelem)
        stair_width = [0] * maxlevels
        node = head
        for level in top_to_bottom:
            while not newelem < node[NEXT][level][VALUE]:
                stair_width[level] += node[WIDTH][level]
                node = node[NEXT][level]
            staircase[level] = node

        # make a new node or reuse one that was previously removed
        if oldnode is None:
            d = min(maxlevels, 1 - int(log(random(), 2.0)))
            newnode = [newelem, [None]*d, [None]*d]
        else:
            newnode = oldnode
            newnode[VALUE] = newelem
            d = len(newnode[NEXT])

        # insert a link to the newnode at each level
        steps = 0
        for level in bottom_to_top[:d]:
            prevnode = staircase[level]
            newnode[NEXT][level] = prevnode[NEXT][level]
            prevnode[NEXT][level] = newnode
            newnode[WIDTH][level] = prevnode[WIDTH][level] - steps
            prevnode[WIDTH][level] = steps
            steps += stair_width[level]
        for level in bottom_to_top:
            prevnode = staircase[level]
            prevnode[WIDTH][level] += 1
        
        if len(queue) >= n:
            # find and yield the midpoint value
            i = midpoint + 1
            node = head
            for level in top_to_bottom:
                while node[WIDTH][level] <= i:
                    i -= node[WIDTH][level]
                    node = node[NEXT][level]
            yield node[VALUE]

            # staircase: first node on each level where node[NEXT][level][VALUE] >= oldelem
            oldelem = queue_popleft()
            node = head
            for level in top_to_bottom:
                while node[NEXT][level][VALUE] < oldelem:
                    node = node[NEXT][level]
                staircase[level] = node
            oldnode = staircase[0][NEXT][0]     # node where oldnode[VALUE] is oldelem

            # remove links to the oldnode
            d = len(oldnode[NEXT])
            for level in bottom_to_top[:d]:
                prevnode = staircase[level]
                prevnode[WIDTH][level] += oldnode[WIDTH][level]
                prevnode[NEXT][level] = oldnode[NEXT][level]
            for level in bottom_to_top:
                prevnode = staircase[level]
                prevnode[WIDTH][level] -= 1


if __name__ == '__main__':

    ###########################################################################
    # Demonstrate the running_median() generator
    # Compare results to an alternative generator
    # implemented by sorting a regular list.

    from bisect import insort
    from random import randrange
    from itertools import islice

    def running_median_slow(n, iterable):
        'Slow running-median with O(n) updates where n is the window size'
        it = iter(iterable)
        queue = deque(islice(it, n))
        sortedlist = sorted(queue)
        midpoint = len(queue) // 2
        yield sortedlist[midpoint]
        for newelem in it:
            oldelem = queue.popleft()
            sortedlist.remove(oldelem)
            queue.append(newelem)
            insort(sortedlist, newelem)
            yield sortedlist[midpoint]

    M, N, window = 9000, 80000, 10001
    data = [randrange(M) for i in range(N)]
    result = list(running_median(window, data))
    expected = list(running_median_slow(window, data))
    assert result == expected
    print 'Successful test of RunningMedian() with', N,
    print 'items and a window of size', window, '\n'
