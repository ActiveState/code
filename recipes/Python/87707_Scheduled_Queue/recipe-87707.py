"""
A scheduled queue is a queue with priorities that are scheduled. It is not preemtitive, higher priorities are not
executed always before than lower priorities (only more often).
USAGE:
init args:
maxsize: maximum size of the queue, if maxsize<=0 then the queue size is infinite
realtime: if true then the queue has a priority REAL_TIME. REAL_TIME priorities are executed before any other priorities.items
idle: if true then the queue has a priority IDLE. IDLE priorities are executed when there are no other priorities left.
priorities: a dictionary with the definitions of the priorities. The key defines the priority name and the value (an int>0)
            defines the relative importance of the priority. A higher number implies that the priority will be checked first more often.
            In this implementation:
            36 = VERY_HIGH + HIGH + ABOVE_DEFAULT + BELOW_DEFAULT + DEFAULT + BELOW_DEFAULT + LOW + VERY_LOW
            VERY_HIGH priorities are checked first 10/36 times
            VERY_LOW only of 1/36
            Of every 36 gets at least one will be VERY_LOW (if VERY_LOW queue is not empty). Even if there are higher non
            empty queue of higher priority VERY_LOW will be checked once every 36 gets.
"""

from Queue import Queue, Full, Empty

#standard priorities
REAL_TIME       = 999
VERY_HIGH       = 10
HIGH            = 8
ABOVE_DEFAULT   = 6
DEFAULT         = 5
BELOW_DEFAULT   = 4
LOW             = 2
VERY_LOW        = 1
IDLE            = -1

standard_priorities = {VERY_HIGH        :10,
                       HIGH             :8,
                       ABOVE_DEFAULT    :6,
                       DEFAULT          :5,
                       BELOW_DEFAULT    :4,
                       LOW              :2,
                       VERY_LOW         :1}

class ScheduledQueue(Queue):
    def __init__(self, maxsize=0, priorities = standard_priorities, realtime = 1, idle = 1):
        """Initialize a queue object with a given maximum size.

        If maxsize is <= 0, the queue size is infinite.
        priorities: a dictionary with definition of priorities
        """
        assert self._check_priorities(priorities)       #check only if not -OO
        import thread
        self._init(priorities, maxsize, realtime, idle)
        self.mutex = thread.allocate_lock()
        self.esema = thread.allocate_lock()
        self.esema.acquire()
        self.fsema = thread.allocate_lock()

    def put(self, item, priority = DEFAULT, block=1):
        """Put an item into the queue.

        If optional arg 'block' is 1 (the default), block if
        necessary until a free slot is available.  Otherwise (block
        is 0), put an item on the queue if a free slot is immediately
        available, else raise the Full exception.
        """
        assert self._queues.has_key(priority),"inexistent priority "+str(priority)
        self._acquirePUT(block)
        was_empty = self._empty()
        try:
            self._put(item, priority)
        finally:
            self._releasePUT(was_empty)

    def put_nowait(self, item, priority = DEFAULT):
        """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.put(item, priority, 0)

    def get(self, block=1):
        """Remove and return an item from the queue.

        If optional arg 'block' is 1 (the default), block if
        necessary until an item is available.  Otherwise (block is 0),
        return an item if one is immediately available, else raise the
        Empty exception.
        """
        self._acquireGET(block)
        was_full = self._full()
        try:
            item = self._get()
        finally:
            self._releaseGET(was_full)        
        return item


    def drain(self):
        self.mutex.acquire()
        self._drain()
        self.mutex.release()
        
    def _acquirePUT(self, block):
        if block:
            self.fsema.acquire()
        elif not self.fsema.acquire(0):
            raise Full
        self.mutex.acquire()

    def _acquireGET(self, block):
        if block:
            self.esema.acquire()
        elif not self.esema.acquire(0):
            raise Empty
        self.mutex.acquire()
        was_full = self._full()        
        
    def _releasePUT(self, was_empty):
        if was_empty:
            self.esema.release()
        if not self._full():
            self.fsema.release()
        self.mutex.release()

    def _releaseGET(self, was_full):
        if was_full:
            self.fsema.release()
        if not self._empty():
            self.esema.release()
        self.mutex.release()  
        
    def __len__(self):
        return self.qsize()
    
    # Override these methods to implement other queue organizations
    # (e.g. stack or priority queue).
    # These will only be called with appropriate locks held
    def _qsize(self):
        return self._len

    def _empty(self):
        """Check whether the queue is empty"""
        return not self._len

    def _full(self):
        """Check whether the queue is full"""
        return self.maxsize > 0 and self._len >= self.maxsize

    def _put(self, item, priority):
        """Put a new item in the queue"""
        self._queues[priority].append(item)
        self._len += 1

    # Get an item from the queue
    def _get(self):
        item = filter(None,self._roundRobinQueues.get())[0].pop(0)
        self._len -= 1
        return item

    def _drain(self):
        for queue in self._queues.values():
            while len(queue)>0:queue.pop()
        self._len = 0    

    # Initialize the queue representation
    def _init(self, priorities, maxsize, realtime, idle):
        self.maxsize = maxsize
        self._index = 0
        self._len = 0
        self._queues = self._buildDictQueues(priorities, realtime, idle)
        self._roundRobinQueues = RoundRobin(self._buildMatrix(priorities))
        self._drain()

    def _buildDictQueues(self, priorities, realtime, idle):
        result = {}
        if realtime: result[REAL_TIME] = [REAL_TIME]
        if idle: result[IDLE] = [IDLE]
        for key in priorities.keys():
            result[key]=[key]
        return result

    def _buildMatrix(self, priorities):
        result = []
        _list = self._buildQueueList(priorities)
        for i in index(_list):
            result.append((remove_duplicates(_list[i:]+ _list[:i])))
        self._addRealTimeIdle2Matrix(result)
        return matrix2tuple(result)

    
    def _buildQueueList(self, priorities):
        result = []
        for key, value in priorities.items():
            for i in range(value):
                result.append(self._queues[key])
        return shuffle_list(result)
    
    def _addRealTimeIdle2Matrix(self, matrix):
        realtime = self._queues.has_key(REAL_TIME)
        idle = self._queues.has_key(IDLE)
        if not realtime and not idle:return
        for row in matrix:
            if realtime:
                row.insert(0,self._queues[REAL_TIME])
            if idle:
                row.append(self._queues[IDLE])

    def _check_priorities(self, priorities):
        for value in priorities.values():
            assert value>0 and type(value)==type(1),"Incorrect definition of priorities"+str(priorities)
        return 1


#utility classes and methods
def index(list):
    return range(len(list))

def index_list(list):
	return zip(index(list),list)
             
def matrix2tuple(matrix):
    for i,row in index_list(matrix):
        matrix[i]=tuple(row)
    return tuple(matrix)

def shuffle_list(_list):
    import random
    for i in index(_list):
        j = int(random.random()*len(_list))
        
        _list[i],_list[j]=_list[j],_list[i]
    return _list

def remove_duplicates(list):
    assert type(list)==type([]) or type(list)==type(()), "List should be a [] or ()"
    result = []
    for elem in list:
        if elem not in result:result.append(elem)
    if type(list)==type(()):result=tuple(result)
    return result

class RoundRobin:
    def __init__(self, round_robin_list):
        assert len(round_robin_list), str(round_robin_list)
        self._index = -1
        self._list = tuple(round_robin_list)
        self._size = len(self._list)
        
    def get(self):
        self._index += 1
        self._index %= self._size
        return self._list[self._index]

#tests
def _test():
    q = ScheduledQueue()
    _empty_test()
    _idle_last()
    _real_first()
    _max_size_test()

def _empty_test(q = ScheduledQueue()):
    try:
        q.get(0)
    except Empty:
        print "Empty test OK"
        
def _idle_last(q = ScheduledQueue()):
    q.put(0,IDLE)
    q.put(1)
    q.get()
    if not q.get():print "IDLE LAST OK"

def _real_first(q = ScheduledQueue()):
    q.put(0)
    q.put(1,REAL_TIME)
    if q.get():print "REAL_TIME test OK"
    q.get()
    
def _max_size_test(q = ScheduledQueue(maxsize = 1)):
    q.put(0)
    try:
        q.put(0, block=0)
    except Full:
        print "Full test OK"

if __name__=='__main__':
    _test()
