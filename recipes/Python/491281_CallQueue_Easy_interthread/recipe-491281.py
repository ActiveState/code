def example_CallQueue():
    # 3 default consumer threads work and collect on 6 I/O jobs
    import urllib,time
    l=['http://www.python.org/',
       'http://www.python.org/about/gettingstarted',
       'http://www.python.org/about/apps/',
       'http://www.python.org/about/quotes',
       'http://www.python.org/about/website',
       'http://www.python.org/about/help', ]
    def work(url):
        return len(urllib.urlopen(url).read())
    #
    cq=CallQueue(max_default_consumer_threads=3)
    for url in l:
        cqitem=cq.call_and_collect(work,(url,))      #schedule
    while not cq.is_done():
        for cqitem in cq.get_next_collected():       #harvest
            print cqitem.args, cqitem.get_return()
        print ".",
        time.sleep(0.001)
    print "example_CallQueue done."

def example2_CallQueue():
    # interacts with my_thread and finally kills it ..
    import sys,thread,time,copy,random
    cq=CallQueue()
    l=[]            # to be filled by my_thread
    def my_thread():
        try: 
            while 1:
                cq.receive()
                l.append(random.random())
        finally:
            print "my_thread terminated."
    thread.start_new(my_thread,())
    time.sleep(0.020)
    l_snapshot=cq.call(lambda:copy.copy(l),wait=1)  #synchronous call
    print "1st snapshot:", len(l_snapshot),"numbers"
    cqitem=cq.call(lambda:copy.copy(l))             #non-blocking call
    while 1:
        if cqitem.is_done():
            l_snapshot2=cqitem.get_return()
            print "2n snapshot:", len(l_snapshot2),"numbers"
            break
        else:
            print ".",
            time.sleep(0.001)
    cq.call(sys.exit, wait=1, raise_exception=2)    #raises SystemExit inside my_thread
    print "end state:",len(l),"numbers"
    print "example2_CallQueue done."


import sys
from time import time as _time, sleep as _sleep

class Full(Exception):pass
class Empty(Exception):pass

class CQItem:
    args=None
    kwargs=None
    done=0              # 1=return value; 2=exception
    delivered=0
    raise_exception=1
    def get_return(self,alt_return=None):
        """delivers the return value or (by default) echoes the exception of the call job
        """
        if self.done==2:
            if self.raise_exception & 1:    #by default exception is raised
                exc=self.exc
                del self.exc
                raise exc[0],exc[1],exc[2]
            else:
                return alt_return
        return self.ret
    def get_exception(self):
        return self.exc
    def is_done(self):
        """returns 1, if the call return's a value; 2, if an exception was raised
        """
        return self.done

class CallQueue:
    closed=0
    exc=None
    max_dthreads=0
    dthreads_count=0
    def __init__(self,maxsize=None,max_default_consumer_threads=0):
        self.fifo=[]            # self.fifo=Queue.Queue() not necessary, if .append() and .pop(0) Python atomic
        self.collected=[]
        self.maxsize=maxsize    # approximate guarantee, if Queue.Queue is not used
        self.max_dthreads=max_default_consumer_threads
    def call( self, func, args=(), kwargs={}, wait=0, timeout=None, raise_exception=1, alt_return=None ):
        """Puts a call into the queue and optionally waits for return.
        
        wait:  0=asynchronous call. A call queue item is returned
               1=waits for return value or exception
               callable -> waits and wait()-call's while waiting for return
        raise_exception: 1=raise in caller, 2=raise in receiver, 3=raise in both, 
                         0=silent replace with alt_return
        """
        if self.dthreads_count<self.max_dthreads:
            self.add_default_consumer_threads(n=1)
        if self.closed:
            raise Full, "queue already closed"
        cqitem=CQItem()
        cqitem.func=func
        cqitem.args=args
        cqitem.kwargs=kwargs
        cqitem.wait=wait
        cqitem.raise_exception=raise_exception
        if self.maxsize and len(self.fifo)>=self.maxsize:
            raise Full, "queue's maxsize exceeded"
        self.fifo.append( cqitem )
        if self.closed:
            raise Full, "queue already closed"
        if wait:
            starttime = _time()
            delay=0.0005
            while not cqitem.is_done():
                if timeout:
                    remaining = starttime + timeout - _time()
                    if remaining <= 0:  #time is over and no element arrived
                        if raise_exception:
                            raise Empty, "return timed out"
                        else:
                            return alt_return
                    delay = min(delay * 2, remaining, .05)
                else:
                    delay = min(delay * 2, .05)
                if callable(wait): wait()
                _sleep(delay)       #reduce CPU usage by using a sleep
            return cqitem.get_return()
        return cqitem
    def call_and_collect(self,*args,**kwargs):
        r=self.call(*args,**kwargs)
        self.collected.append(r)
        return r
    def add_default_consumer_threads(self,n=1,maxdelay=0.016):
        import thread, weakref
        weak_self=weakref.proxy(self)
        for i in range(n):
            self.dthreads_count+=1
            tid=thread.start_new(_default_consumer_thread,(weak_self,maxdelay))
    def is_done(self):
        """check if call-queue and collected are flushed"""
        if self.fifo or self.collected:
            return False
        return True
    def get_next_collected(self):
        next=[]
        for cqitem in self.collected[:]:
            if not isinstance(cqitem,CQItem) or cqitem.is_done():
                next.append(cqitem)
                self.collected.remove(cqitem)
        return next

    def receive(self):
        """To be called (periodically) by target thread(s). Returns number of calls handled.
        """
        count=0
        while self.fifo:
            try:
                cqitem=self.fifo.pop(0)
            except IndexError:
                break  # multi-consumer race lost
            try:
                cqitem.ret=cqitem.func(*cqitem.args,**cqitem.kwargs)
                cqitem.done=1
            except:
                if cqitem.raise_exception & 1:
                    cqitem.exc=sys.exc_info()
                cqitem.done=2
                if cqitem.raise_exception & 2:
                    raise
            count+=1
        return count
            
    def qsize(self):
        """Returns current number of unconsumed calls in the queue
        """
        return len(self.fifo)
    def close(self):
        """stops further attempts for calling and terminates default consumer threads
        """
        self.closed=1
    def close_and_receive_last(self):
        self.close()
        self.receive()
    def __del__(self):
        self.close()

def _default_consumer_thread(cq,maxdelay=0.016):
    delay=0.001
    try: 
        while not cq.closed:
            count=cq.receive()
            if count: delay=0.001
            _sleep(delay)
            delay=min(delay*2,maxdelay)
    except ReferenceError:
        pass

if __name__=='__main__':
    example_CallQueue()
    example2_CallQueue()
