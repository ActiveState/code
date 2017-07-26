class Clock(object):
    # Get a private copy of the time module
    _time = __import__('time')

    def __init__(self, rate=1):
        self.rate = rate
        
        # Initialize the real and virtual current time
        self.time = self.start = self._time.time()


    def getCurrentTimestamp(self):
        # Compute the elapsed real time
        now = self._time.time() 
        d =  now - self.time

        # Update the real and virtual current time
        self.time = now
        self.start = self.start + d * self.rate

        return self.start

    def setCurrentTime(self, timestamp):
        self.start = self._time.mktime(timestamp.timetuple())


class TimeHook(object):
    # Get a private copy of the time module
    _time = __import__('time')

    def __init__(self, clock):
        """Install the hook, using the given Clock implementation to
        obtain the current time.
        """

        import sys

        self.clock = clock
        sys.modules['time'] = self


    def asctime(self, t=None):
        if t is None:
            t = self.localtime()

        return self._time.asctime(t)

    def ctime(self, secs=None):
        if secs is None:
            secs = self.time()
        
        return self._time.ctime(secs)

    def gmtime(self, secs=None):
        if secs is None:
            secs = self.time()

        return self._time.gmtime(secs)

    def localtime(self, secs=None):
        if secs is None:
            secs = self.time()

        return self._time.localtime(secs)

    def time(self):
        return self.clock.getCurrentTimestamp()

    def __getattr__(self, name):
        return getattr(self._time, name)


if __name__ == '__main__':
    # Install the hook
    clock = Clock(rate=60*60)
    TimeHook(clock)


    # We need to import the time module after the initialization of
    # the hook
    import time
    import datetime


    clock.setCurrentTime(datetime.datetime(1999, 12, 31, 22))
    for i in range(4):
        print datetime.datetime.fromtimestamp(time.time())
        print datetime.datetime.now() # TODO does not works
        print datetime.date.today()
        print '-' * 26
        
        time.sleep(1)
