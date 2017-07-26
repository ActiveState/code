from __future__ import generators
import threading

class SpawnedGenerator(threading.Thread):
    "Class to spawn a generator."

    def __init__(self, generator, queueSize=0):
        "Initialise the spawned generator from a generator."
        threading.Thread.__init__(self)
        self.generator = generator
        self.queueSize = queueSize

    def stop(self):
        "Request a stop."
        self.stopRequested = 1

    def run(self):
        "Called in a separate thread by Thread.start()."
        queue = self.queue
        try:
            it = iter(self.generator)
            while 1:
                next = it.next()
                queue.put((1, next)) # will raise StopIteration
                if self.stopRequested:
                    raise StopIteration, "stop requested"
        except:
            queue.put((0, sys.exc_info()))

    def __call__(self):
        "Yield results obtained from the generator."
        self.queue = queue = Queue.Queue(self.queueSize)
        self.stopRequested = 0
        self.start() # run() will stuff the queue in a separate Thread 
        keepGoing, item = queue.get()
        while keepGoing:
            yield item
            keepGoing, item = queue.get()
        # if keepGoing is false, item is exc_info() result
        self.exc_info = item # stash it for the curious
        type, value, traceback = item
        if isinstance(type, StopIteration):
            return
        else:
            raise type, value, traceback

    def __iter__(self):
        "Return an iterator for our executed self."
        return iter(self())
