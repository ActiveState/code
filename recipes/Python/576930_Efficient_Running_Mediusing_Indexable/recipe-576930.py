from random import random
from math import log, ceil

class Node(object):
    __slots__ = 'value', 'next', 'width'
    def __init__(self, value, next, width):
        self.value, self.next, self.width = value, next, width

class End(object):
    'Sentinel object that always compares greater than another object'
    def __cmp__(self, other):
        return 1

NIL = Node(End(), [], [])               # Singleton terminator node

class IndexableSkiplist:
    'Sorted collection supporting O(lg n) insertion, removal, and lookup by rank.'

    def __init__(self, expected_size=100):
        self.size = 0
        self.maxlevels = int(1 + log(expected_size, 2))
        self.head = Node('HEAD', [NIL]*self.maxlevels, [1]*self.maxlevels)

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        node = self.head
        i += 1
        for level in reversed(range(self.maxlevels)):
            while node.width[level] <= i:
                i -= node.width[level]
                node = node.next[level]
        return node.value

    def insert(self, value):
        # find first node on each level where node.next[levels].value > value
        chain = [None] * self.maxlevels
        steps_at_level = [0] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value <= value:
                steps_at_level[level] += node.width[level]
                node = node.next[level]
            chain[level] = node

        # insert a link to the newnode at each level
        d = min(self.maxlevels, 1 - int(log(random(), 2.0)))
        newnode = Node(value, [None]*d, [None]*d)
        steps = 0
        for level in range(d):
            prevnode = chain[level]
            newnode.next[level] = prevnode.next[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] += 1
        self.size += 1

    def remove(self, value):
        # find first node on each level where node.next[levels].value >= value
        chain = [None] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value < value:
                node = node.next[level]
            chain[level] = node
        if value != chain[0].next[0].value:
            raise KeyError('Not Found')

        # remove one link at each level
        d = len(chain[0].next[0].next)
        for level in range(d):
            prevnode = chain[level]
            prevnode.width[level] += prevnode.next[level].width[level] - 1
            prevnode.next[level] = prevnode.next[level].next[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] -= 1
        self.size -= 1

    def __iter__(self):
        'Iterate over values in sorted order'
        node = self.head.next[0]
        while node is not NIL:
            yield node.value
            node = node.next[0]

from collections import deque
from itertools import islice

class RunningMedian:
    'Fast running median with O(lg n) updates where n is the window size'

    def __init__(self, n, iterable):
        self.it = iter(iterable)
        self.queue = deque(islice(self.it, n))
        self.skiplist = IndexableSkiplist(n)
        for elem in self.queue:
            self.skiplist.insert(elem)

    def __iter__(self):
        queue = self.queue
        skiplist = self.skiplist
        midpoint = len(queue) // 2
        yield skiplist[midpoint]
        for newelem in self.it:
            oldelem = queue.popleft()
            skiplist.remove(oldelem)
            queue.append(newelem)
            skiplist.insert(newelem)
            yield skiplist[midpoint]


if __name__ == '__main__':

    #########################################################################
    # Demonstrate the RunningMedian() class
    # Compare results to alternative class implemented using a regular list

    from bisect import insort
    from random import randrange

    class RunningMedianSlow:
        'Slow running-median with O(n) updates where n is the window size'

        def __init__(self, n, iterable):
            self.it = iter(iterable)
            self.queue = deque(islice(self.it, n))
            self.sortedlist = sorted(self.queue)

        def __iter__(self):
            queue = self.queue
            sortedlist = self.sortedlist
            midpoint = len(queue) // 2
            yield sortedlist[midpoint]
            for newelem in self.it:
                oldelem = queue.popleft()
                sortedlist.remove(oldelem)
                queue.append(newelem)
                insort(sortedlist, newelem)
                yield sortedlist[midpoint]

    M, N, window = 5000, 8000, 1001
    data = [randrange(M) for i in range(N)]
    result = list(RunningMedian(window, data))
    expected = list(RunningMedianSlow(window, data))
    assert result == expected
    print 'Successful test of RunningMedian() with', N,
    print 'items and a window of size', window, '\n'


    #########################################################################
    # Demonstrate and test the IndexableSkiplist() collection class

    from random import shuffle

    demo = list('FOURSQUARE')
    excluded = list('XZ')

    print 'Building an indexable skiplist containing %r:' % ''.join(demo)
    s = IndexableSkiplist(len(demo))                        # exercise __init__()
    shuffle(demo)
    for char in demo:
        s.insert(char)                                      # check insert()
        print 'Adding: ', char, list(s), len(s)

    for char in excluded:
        print 'Attempting to remove:', char, '-->',
        try:
            s.remove(char)                                  # check remove() item not in skiplist
        except KeyError:
            print 'Successfully not found'

    assert len(s) == len(demo)                              # check __len__()
    assert list(s) == sorted(demo)                          # check __iter__()
    assert [s[i] for i in range(len(s))] == sorted(demo)    # check __getitem__()

    shuffle(demo)
    for char in demo:
        s.remove(char)                                      # check remove() item in skiplist
        print 'Removing: ', char, list(s), len(s)
    assert list(s) == [] and len(s) == 0


    #############################################################################
    # Show the IndexableSkiplist's internal structure and describe its invariants

    def iter_levels(skiplist, level):
        'Iterate through nodes on a given level.'
        node = skiplist.head
        while node is not NIL:
            yield node
            node = node.next[level]

    demo = list('HOPSCOTCH')                    # create a sample skiplist
    s = IndexableSkiplist(len(demo))
    for char in demo:
        s.insert(char)

    print '\nStructure of an indexable skiplist containing %r:' % ''.join(demo)
    for i in reversed(range(s.maxlevels)):      # show the link structure on each level
        print 'Level %d:  ' % i,
        line = ''
        for n in iter_levels(s, i):
            line += '%s%d %s' % (n.value, n.width[i], '   ' * (n.width[i] - 1))
        print line + 'NIL'

    print '\nNote the following structure invariants:'
    print '* Level 0 has widths all equal to one.'
    print '* The sum of widths on each level == len(skiplist)+1.'
    print '* Entries on higher levels are subsets of the lower levels.'
    print '* Widths of entries on higer levels sum to the widths below.'
    print '    For example, a P --> T link of two steps on one level'
    print '    corresponds to P --> S --> T links of one step each on level 0.'
