import candygram as cg


class Thread:

    """A thread class with just a single counter value and a stop flag."""

    def __init__(self):
        """Initialize counter to zero and stop flag to False."""
        self.val = 0
        self.stop = False

    def increment(self):
        """Increment the counter by one."""
        self.val += 1

    def sendVal(self, msg):
        """Send current value of counter to requesting thread."""
        req = msg[0]
        req.send((cg.self(), self.val))

    def setStop(self):
        """Trip the stop flag."""
        self.stop = True

    def run(self):
        """Entry point of thread."""
        # Register the handler functions for various messages:
        r = cg.Receiver()
        r.addHandler('increment', self.increment)
        r.addHandler((cg.Process, 'value'), self.sendVal, cg.Message)
        r.addHandler('stop', self.setStop)
        # Keep handling new messages until the stop flag is set.
        while not self.stop:
            r.receive()
        # end while


# Create new thread.
counter = cg.spawn(Thread().run)
# Define a receiver that will return the thread's response values:
response = cg.Receiver()
response.addHandler((counter, int), lambda msg: msg[1], cg.Message)
# Tell thread to increment twice.
counter.send('increment')
counter.send('increment')
# Request thread's current value.
counter.send((cg.self(), 'value'))
# Print the response
print response.receive()
# Tell thread to increment one more time.
counter.send('increment')
# And print it's current value.
counter.send((cg.self(), 'value'))
print response.receive()
# Tell thread to stop.
counter.send('stop')
