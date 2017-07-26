import threading
import time

class ThreadGateException(Exception):
    pass

class ThreadGate(object):
    """ A class which works as a FIFO 'gate' for threads. By
    default the gate is open and any thread calling on the
    'enter' method returns immediately.

    A thread can 'close' the gate by calling the method 'close'.
    This thread becomes the owner of the gate. Any other thread
    calling 'enter' after this is automatically blocked till
    the owner calls reopens the gate by calling 'open'.

    The gate requires a certain number of threads to block
    before the owner exits from the 'close' method. Otherwise,
    the owner waits for a timeout before returning from the 'close'
    method, without actually closing the gate.
    
    The gate class can be used to block running threads for a 
    particular operation and making sure that they resume after
    the operation is complete, for a fixed number of threads.
    """

    def __init__(self, numthreads, timeout=0):
        self.lock = threading.Lock()
        self.sem = threading.BoundedSemaphore(1)
        self.evt = threading.Event()
        self.count = 0
        self.owner_timeout = timeout
        self.owner = None
        self.nthreads = numthreads
        # Open by default
        self.position = 1

    def close(self):
        """ Close the gate. The calling thread
        becomes the owner of the gate and blocks
        till the requisite number of threads block
        on the gate or a timeout occurs, whichever
        is first.

        It is an error if the gate is already closed """

        if self.position == 0:
            # Already closed
            raise ThreadGateException,"trying to close an already closed gate"

        try:
            self.lock.acquire()
            self.position = 0
            self.owner = threading.currentThread()
            self.sem.acquire()
        finally:
            self.lock.release()

        # Wait on the event till timeout
        self.evt.clear()
        self.evt.wait(self.owner_timeout)
        
        # If event was set, requisite number off
        # threads have blocked, else reset the gate
        if not self.evt.isSet():
            try:
                print 'Owner thread timedout, re-setting gate'
                self.lock.acquire()
                self.position = 1
                self.owner = None
                self.sem.release()
            finally:
                self.lock.release()

            return -1
            
        return 0

        
    def open(self):
        """ Open the gate. The calling thread should
        be the owner of the gate. It is an error if
        the gate is already open """

        if self.position == 1:
            # Already open
            raise ThreadGateException,"trying to open an already opened gate"

        if threading.currentThread() != self.owner:
            raise ThreadGateException,"not owner, cannot open gate"
            
        try:
            self.lock.acquire()
            self.position = 1
            self.owner = None
            self.sem.release()
        finally:
            self.lock.release()
            
    def enter(self):
        """ Enter the gate. If the gate is open, returns
        immediately, else gets blocked till the gate is
        opened by the owner """

        if self.position==1:
            return 0

        # Lock mutex and increment count
        try:
            self.lock.acquire()
            self.count += 1
            if self.count==self.nthreads:
                self.evt.set()
        finally:
            self.lock.release()

        ct = threading.currentThread()
        print 'Thread %s - Entering Gate' % (ct.getName())

        # Lock mutex and decrement count
        try:
            # Will block here
            self.sem.acquire()
            self.lock.acquire()
            self.count -= 1
        finally:
            self.lock.release()
            self.sem.release()
            
        print 'Thread %s - Exiting Gate' % (ct.getName())
        
    def get_count(self):
        """ Return count of blocked threads """

        return self.count


def test():
    """ Test code """

    import random
    import Queue

    enterlog = Queue.Queue(0)
    exitlog = Queue.Queue(0)

    def enter(index):
        enterlog.put(index)

    def exit(index):
        exitlog.put(index)


    class OwnerThread(threading.Thread):
        """ Owner thread class for gate demo """

        def __init__(self, gate):
            self.gate = gate
            threading.Thread.__init__(self, None, 'Owner thread')
            
        def run(self):
            # Close the gate
            print 'Closing gate...'
            ret = self.gate.close()
            if ret==0:
                print 'Gate closed successfully'

            print 'Gate count=>',self.gate.get_count()
                
            # Open gate after sleeping some time
            time.sleep(5)
            if ret==0:
                print 'Opening gate'
                self.gate.open()
            else:
                print 'Gate closing not successful'

            
    class SampleThread(threading.Thread):
        """ Sample thread class for gate demo """
        
        def __init__(self, index, gate):
            self.gate = gate
            self.index = index
            threading.Thread.__init__(self, None, 'Thread %d' % self.index, None) 
                                      
        def run(self):

            # Sleep randomly
            time.sleep(random.choice(range(1,10)))
            # Mark entry to gate
            enter(self.index)
            self.gate.enter()
            # Mark exit out of gate
            exit(self.index)


    def test1():
        """ Test code where gate is closed successfully """

        print 'test1()...'

        gate = ThreadGate(10, 20)
        
        random.seed()
        
        print 'Starting threads...'
        # Create 10 threads
        threads = []
        threads.append(OwnerThread(gate))
        
        for x in range(10):
            threads.append(SampleThread(x, gate))
            
        # Start threads and join
        for x in range(11):
            threads[x].start()        
            

        # Join with threads
        for x in range(11):
            threads[x].join()

        print 'Joined with threads'
        print 'Gate count=>',gate.get_count()
            
        # Exit and entry logs must be same
        print enterlog
        print exitlog

    def test2():
        """ Test code where gate is closed unsuccessfully """

        print 'test1()...'

        gate = ThreadGate(10, 5)
        
        random.seed()
        
        print 'Starting threads...'
        # Create 10 threads
        threads = []
        threads.append(OwnerThread(gate))
        
        for x in range(10):
            threads.append(SampleThread(x, gate))
            
        # Start threads and join
        for x in range(11):
            threads[x].start()        
            

        # Join with threads
        for x in range(11):
            threads[x].join()

        print 'Joined with threads'

        print 'Gate count=>',gate.get_count()
        
        # Exit and entry logs must be same
        print enterlog
        print exitlog        

    test1()

    while not enterlog.empty():
        print enterlog.get(),

    print

    while not exitlog.empty():
        print exitlog.get(),
        
    print
    
    test2()

    while not enterlog.empty():
        print enterlog.get(),

    print

    while not exitlog.empty():
        print exitlog.get(),
        
    print
    
    
if __name__ == "__main__":
    test()
            
