def iter_except(func, exception, start=None):
    'Yield a function repeatedly until it raises an exception'
    try:
        if start is not None:
            yield start()
        while 1:
            yield func()
    except exception:
        pass



### Examples ####################################################

if __name__ == '__main__':

    # Example using BSDDB's last() and next() methods
    import bsddb
    db = bsddb.btopen('/tmp/spam.db', 'c')
    for i in range(10):
        db['%d'%i] = '%d'% (i*i)
    for k, v in iter_except(db.next, bsddb.error, start=db.first):
        print k, v


    # Example of fetching tasks from a priority queue
    from random import random
    from heapq import heappush, heappop
    from functools import partial
    pq = []
    for i in range(10):
        heappush(pq, (random(), 'task %d' % i))
    for priority, task in iter_except(partial(heappop, pq), IndexError):
        print priority, task


    # Example of atomic, destructive reads from a dictionary
    d = dict(enumerate('abcdefghi'))
    for k, v in iter_except(d.popitem, KeyError):
        print k, v

    # Example of atomic, destructive reads from a deque
    import collections
    d = collections.deque('abcdefghi')
    for v in iter_except(d.popleft, IndexError):
        print v


    # Example of iterating over a producer Queue:
    import Queue
    q = Queue.Queue()
    for i in range(10):
        q.put('*' * i)
    for v in iter_except(q.get_nowait, Queue.Empty):
        print v


    # Example of iterating destructively over a set
    s = set('abracadabra')
    for elem in iter_except(s.pop, KeyError):
        print elem
