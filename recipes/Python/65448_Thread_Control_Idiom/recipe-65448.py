#!/usr/bin/env python
"""
testthread.py
An example of an idiom for controling threads

Doug Fort
http://www.dougfort.net
"""

import threading

class TestThread(threading.Thread):
    """
    A sample thread class
    """
        
    def __init__(self):
        """
        Constructor, setting initial variables
        """
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name="TestThread")
        
    def run(self):
        """
        overload of threading.thread.run()
        main control loop
        """
        print "%s starts" % (self.getName(),)
        
        count = 0
        while not self._stopevent.isSet():
            count += 1
            print "loop %d" % (count,)
            self._stopevent.wait(self._sleepperiod)
        
        print "%s ends" % (self.getName(),)

    def join(self,timeout=None):
        """
        Stop the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)

if __name__ == "__main__":
    testthread = TestThread()
    testthread.start()
    
    import time
    time.sleep(10.0)

    testthread.join()
    
