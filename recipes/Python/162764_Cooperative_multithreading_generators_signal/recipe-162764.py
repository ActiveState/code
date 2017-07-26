from __future__ import generators

import signal

# An implementation of cooperative multithreading using generators
# that handles signals; by Brian O. Bush

# credit: based off an article by David Mertz
# http://gnosis.cx/publish/programming/charming_python_b7.txt

def empty():
    """ This is an empty task. """
    while True:
        print "<empty process>"
        yield None
        
def delay(duration):
    import time
    while True:
        print "<sleep %d>" % duration
        time.sleep(duration)
        yield None

class GenericScheduler:
    def __init__(self):
        signal.signal(signal.SIGINT, self.shutdownHandler)
        self.shutdownRequest = False
        self.threads = []
        # add some "processes"
        self.threads.append(delay(1))
        self.threads.append(delay(2))
        self.threads.append(empty())
    def shutdownHandler(self, n, frame):
        """ Initiate a request to shutdown cleanly on SIGINT."""
        print "Request to shut down."
        self.shutdownRequest = True        
    def scheduler(self):
        try:
            while 1:
                map(lambda t: t.next(), self.threads)
                if self.shutdownRequest:
                    break
        except StopIteration:
            pass

if __name__== "__main__":
    s = GenericScheduler()
    s.scheduler()
