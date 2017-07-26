def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

if __name__ == '__main__':
    from threading import Thread, Lock
    import time

    myLock = Lock()

    class MyThread(Thread):
        def __init__(self, n):
            Thread.__init__(self)
            self.n = n

        @synchronized(myLock)
        def run(self):
            """ Print out some stuff.

            The method sleeps for a second each iteration.  If another thread
            were running, it would execute then.
            But since the only active threads are all synchronized on the same
            lock, no other thread will run.
            """

            for i in range(5):
                print 'Thread %d: Start %d...' % (self.n, i),
                time.sleep(1)
                print '...stop [%d].' % self.n

    threads = [MyThread(i) for i in range(10)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
