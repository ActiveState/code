from threading import Thread, Event, Timer
import time

def TimerReset(*args, **kwargs):
    """ Global function for Timer """
    return _TimerReset(*args, **kwargs)


class _TimerReset(Thread):
    """Call a function after a specified number of seconds:

    t = TimerReset(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
        self.resetted = True

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        print "Time: %s - timer running..." % time.asctime()

        while self.resetted:
            print "Time: %s - timer waiting for timeout in %.2f..." % (time.asctime(), self.interval)
            self.resetted = False
            self.finished.wait(self.interval)

        if not self.finished.isSet():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
        print "Time: %s - timer finished!" % time.asctime()

    def reset(self, interval=None):
        """ Reset the timer """

        if interval:
            print "Time: %s - timer resetting to %.2f..." % (time.asctime(), interval)
            self.interval = interval
        else:
            print "Time: %s - timer resetting..." % time.asctime()

        self.resetted = True
        self.finished.set()
        self.finished.clear()



#
# Usage examples
#
def hello():
    print "Time: %s - hello, world" % time.asctime()

# No reset
print "Time: %s - start..." % time.asctime()
tim = TimerReset(5, hello)
tim.start()
print "Time: %s - sleeping for 10..." % time.asctime()
time.sleep (10)
print "Time: %s - end..." % time.asctime()

print "\n\n"

# With Reset
print "Time: %s - start..." % time.asctime()
tim = TimerReset(5, hello)
tim.start()
print "Time: %s - sleeping for 4..." % time.asctime()
time.sleep (4)
tim.reset()
print "Time: %s - sleeping for 10..." % time.asctime()
time.sleep (10)
print "Time: %s - end..." % time.asctime()

print "\n\n"

# With reset interval
print "Time: %s - start..." % time.asctime()
tim = TimerReset(5, hello)
tim.start()
print "Time: %s - sleeping for 4..." % time.asctime()
time.sleep (4)
tim.reset (9)
print "Time: %s - sleeping for 10..." % time.asctime()
time.sleep (10)
print "Time: %s - end..." % time.asctime()


#
# Output of test program
#
Time: Fri Sep 24 15:31:16 2010 - start...
Time: Fri Sep 24 15:31:16 2010 - timer running...
Time: Fri Sep 24 15:31:16 2010 - timer waiting for timeout in 5.00...
Time: Fri Sep 24 15:31:16 2010 - sleeping for 10...
Time: Fri Sep 24 15:31:21 2010 - hello, world
Time: Fri Sep 24 15:31:21 2010 - timer finished!
Time: Fri Sep 24 15:31:26 2010 - end...



Time: Fri Sep 24 15:31:26 2010 - start...
Time: Fri Sep 24 15:31:26 2010 - timer running...
Time: Fri Sep 24 15:31:26 2010 - timer waiting for timeout in 5.00...
Time: Fri Sep 24 15:31:26 2010 - sleeping for 4...
Time: Fri Sep 24 15:31:30 2010 - timer resetting...
Time: Fri Sep 24 15:31:30 2010 - sleeping for 10...
Time: Fri Sep 24 15:31:30 2010 - timer waiting for timeout in 5.00...
Time: Fri Sep 24 15:31:35 2010 - hello, world
Time: Fri Sep 24 15:31:35 2010 - timer finished!
Time: Fri Sep 24 15:31:40 2010 - end...



Time: Fri Sep 24 15:31:40 2010 - start...
Time: Fri Sep 24 15:31:40 2010 - timer running...
Time: Fri Sep 24 15:31:40 2010 - timer waiting for timeout in 5.00...
Time: Fri Sep 24 15:31:40 2010 - sleeping for 4...
Time: Fri Sep 24 15:31:44 2010 - timer resetting to 9.00...
Time: Fri Sep 24 15:31:44 2010 - sleeping for 10...
Time: Fri Sep 24 15:31:44 2010 - timer waiting for timeout in 9.00...
Time: Fri Sep 24 15:31:53 2010 - hello, world
Time: Fri Sep 24 15:31:53 2010 - timer finished!
Time: Fri Sep 24 15:31:54 2010 - end...
