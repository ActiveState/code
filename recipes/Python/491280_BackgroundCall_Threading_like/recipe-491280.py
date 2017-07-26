def example_BackgroundCall():
    import urllib,time
    def work():
        return urllib.urlopen('http://www.python.org/').read()
    bkcall=BackgroundCall(work)
    print 'work() executing in background ...'
    while not bkcall.is_done():
        print '.',
        time.sleep(0.010)
    print 'done.'
    print bkcall.get_return()[:500]

import sys
from time import time as _time, sleep as _sleep

class Full(Exception):pass
class Empty(Exception):pass

class BackgroundCall:
    """BackgroundCall

    Example:
        bkcall=BackgroundCall( time_consuming_function )
        ...
        if bkcall.is_done():
            print "got", bkcall.get_return()
    """
    id=None
    done=0      #1=returned; 2=exception raised
    def __init__(self, func, args=(), kwargs={}):
        import thread
        def thread_bkcall():
            try:
                self.ret=func(*args, **kwargs)
                self.done=1
            except:
                self.exc=sys.exc_info()
                self.done=2
        self.id=thread.start_new(thread_bkcall, ())
    def is_done(self):
        return self.done
    def get_return(self, wait=1, timeout=None, raise_exception=1, alt_return=None):
        """delivers the return value or (by default) echoes the exception of 
           the call job

           wait: 0=no waiting; Attribute error raised if no
                 1=waits for return value or exception
                 callable -> waits and wait()-call's while waiting for return
        """
        if not self.done and wait:
            starttime=_time()
            delay=0.0005
            while not self.done:
                if timeout:
                    remaining = starttime + timeout - _time()
                    if remaining <= 0:  #time is over
                        if raise_exception:
                            raise Empty, "return timed out"
                        else:
                            return alt_return
                    delay = min(delay * 2, remaining, .05)
                else:
                    delay = min(delay * 2, .05)
                if callable(wait): wait()
                _sleep(delay)       #reduce CPU usage by using a sleep
        if self.done==2:    #we had an exception
            exc=self.exc
            del self.exc
            if raise_exception & 1:    #by default exception is raised
                raise exc[0],exc[1],exc[2]
            else:
                return alt_return
        return self.ret
    def get_exception(self):
        return self.exc

if __name__=='__main__':
    example_BackgroundCall()
