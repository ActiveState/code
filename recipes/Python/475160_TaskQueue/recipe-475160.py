import threading
from Queue import Queue

class TaskQueue(Queue):

    def __init__(self):
        Queue.__init__(self)        
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0

    def _put(self, item):
        Queue._put(self, item)
        self.unfinished_tasks += 1        

    def task_done(self):
        """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """
        self.all_tasks_done.acquire()
        try:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notifyAll()
            self.unfinished_tasks = unfinished
        finally:
            self.all_tasks_done.release()

    def join(self):
        """Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        self.all_tasks_done.acquire()
        try:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()
        finally:
            self.all_tasks_done.release()


#### Example code ####################

import sys

def worker():
    'Stop at 1; otherwise if odd then load 3*x+1; or if even then divide by two'
    name = threading.currentThread().getName()
    while True:
        x = q.get()
        sys.stdout.write('%s\t%d\n' % (name, x))
        if x <= 1:
            sys.stdout.write('!\n')
        elif x % 2 == 1:
            q.put(x * 3 + 1)
        else:
            q.put(x // 2)
        q.task_done()

q = TaskQueue()
numworkers = 4
for i in range(numworkers):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

for x in range(1, 50):
    q.put(x)

q.join()
print 'All inputs found their way to 1.  Queue is empty and all processing complete.'
