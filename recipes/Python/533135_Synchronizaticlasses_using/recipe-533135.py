# Synchronization classes using decorators. Provides synchronized, semaphore
# and event classes which provide transparent decorator patterns for
# Lock, BoundedSemaphore and Event objects in Python.

from threading import Thread, Lock, BoundedSemaphore, Event, currentThread
from time import sleep
from random import random
    
class synchronized(object):
    """ Class enapsulating a lock and a function
    allowing it to be used as a synchronizing
    decorator making the wrapped function
    thread-safe """
    
    def __init__(self, *args):
        self.lock = Lock()
        
    def __call__(self, f):
        def lockedfunc(*args, **kwargs):
            try:
                self.lock.acquire()
                print 'Acquired lock=>',currentThread()
                try:
                    return f(*args, **kwargs)
                except Exception, e:
                    raise
            finally:
                self.lock.release()
                print 'Released lock=>',currentThread()

        return lockedfunc


class semaphore(object):
    """ Class encapsulating a semaphore to limit
    number of resources  """

    def __init__(self, *args):
        self.sem = BoundedSemaphore(args[0])
    
    def __call__(self, f):
        def semfunc(*args, **kwargs):
            try:
                print 'Trying to acquire sem=>',currentThread()
                self.sem.acquire()
                print 'Acquired sem=>',currentThread()
                try:
                    return f(*args, **kwargs)
                except Exception, e:
                    raise
            finally:
                self.sem.release()
                print 'Released sem=>',currentThread()

        
        return semfunc

class event(object):
    """ Class encapsulating an event object to control
    sequential access to a resource """

    def __init__(self, *args):
        self.evt = Event()
        self.evt.set()
    
    def __call__(self, f):
        def eventfunc(*args, **kwargs):
            try:
                print 'Waiting on event =>',currentThread()
                self.evt.wait()
                # First thread will clear the event and
                # make others wait, once it is done with the
                # job, it sets the event which wakes up
                # another thread, which does the same thing...
                # This provides sequential access to a
                # resource...
                self.evt.clear()
                print 'Cleared event =>',currentThread()
                try:
                    return f(*args, **kwargs)
                except Exception, e:
                    raise
            finally:
                # Wake up another thread...
                self.evt.set()
                print 'Set event=>',currentThread()

        return eventfunc

##############################################################################
# Test Code                                                                  #
##############################################################################
# Demonstrating the synchronization classes...
# Use a global list

l=range(10)

def reset():
    global l
    l = range(10)

# Not thread-safe        
def func1(begin, end):
    for x in range(begin, end):
        sleep(random()*0.5)
        l.append(x)

# Thread-safe!
@synchronized()
def func2(begin, end):
    for x in range(begin, end):
        sleep(random()*0.5)        
        l.append(x)


# Limited access, thread-safe
class DBConnection(object):
    """ A dummy db connection class """

    MAX = 5
    # We want to limit the number of DB connections to MAX
    # at a given time
    @semaphore(MAX)
    def connect(self, host):
        print "Connecting...",currentThread()
        # Sleep for some time
        sleep(3.0)
        pass

    # We want sequential access to this function
    @event()
    def connect2(self, host):
        print "Connecting...",currentThread()
        # Sleep for some time
        sleep(3.0)
        pass    
    

class PrintMsg(object):
    def startmsg(self):
        print '%s started...' % self.__class__.__name__
    def endmsg(self):
        print '%s ended...' % self.__class__.__name__        

class BaseThread(Thread, PrintMsg):
    pass

class MyThread1(BaseThread):
    def run(self):
        self.startmsg()
        func1(10, 20)
        self.endmsg()        

class MyThread2(BaseThread):
    def run(self):
        self.startmsg()        
        func1(20, 30)
        self.endmsg()

class MyThread3(BaseThread):
    def run(self):
        self.startmsg()
        func2(10, 20)
        self.endmsg()        

class MyThread4(BaseThread):
    def run(self):
        self.startmsg()        
        func2(20, 30)
        self.endmsg()                

class DBThread(BaseThread):
    def run(self):
        db = DBConnection()
        db.connect('localhost')


class DBThread2(BaseThread):
    def run(self):
        db = DBConnection()
        db.connect2('localhost')


print 'Starting the lock test...'

t1 = MyThread1()
t2 = MyThread2()

t1.start(); t2.start()
t1.join(); t2.join()

# List will not have elements in order
print l

reset()

t3 = MyThread3()
t4 = MyThread4()

t3.start(); t4.start()
t3.join(); t4.join()

# List will have elements in order
print l


sleep(3.0)

print 'Starting the sem test...'
# Sem test, init 8 threads and call connect
# on the DBConnection object...
for x in range(8):
   t = DBThread()
   t.start()#

sleep(3.0)

print 'Starting event test..'

# Event test, init 8 threads and 
# increment counter
for x in range(8):
    t = DBThread2()
    t.start()

print 'All tests completed.'
###############################################################################
#  End of test code                                                           #
###############################################################################
