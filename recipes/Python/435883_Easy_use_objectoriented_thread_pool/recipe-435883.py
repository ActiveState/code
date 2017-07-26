__all__ = ['makeRequests', 'NoResultsPending', 'NoWorkersAvailable',
  'ThreadPool', 'WorkRequest', 'WorkerThread']

__author__ = "Christopher Arndt"
__version__ = "1.1"
__date__ = "2005-07-19"

import threading, Queue

class NoResultsPending(Exception):
    """All work requests have been processed."""
    pass
class NoWorkersAvailable(Exception):
    """No worker threads available to process remaining requests."""
    pass

class WorkerThread(threading.Thread):
    """Background thread connected to the requests/results queues.

    A worker thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.
    """

    def __init__(self, requestsQueue, resultsQueue, **kwds):
        """Set up thread in damonic mode and start it immediatedly.

        requestsQueue and resultQueue are instances of Queue.Queue passed
        by the ThreadPool class when it creates a new worker thread.
        """
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self.workRequestQueue = requestsQueue
        self.resultQueue = resultsQueue
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """Repeatedly process the job queue until told to exit.
        """

        while not self._dismissed.isSet():
            # thread blocks here, if queue empty
            request = self.workRequestQueue.get()
            if self._dismissed.isSet():
                # return the work request we just picked up
                self.workRequestQueue.put(request)
                break # and exit
            # XXX catch exceptions here and stick them to request object
            self.resultQueue.put(
                (request, request.callable(*request.args, **request.kwds))
            )

    def dismiss(self):
        """Sets a flag to tell the thread to exit when done with current job.
        """

        self._dismissed.set()


class WorkRequest:
    """A request to execute a callable for putting in the request queue later.

    See the module function makeRequests() for the common case
    where you want to build several work requests for the same callable
    but different arguments for each call.
    """

    def __init__(self, callable, args=None, kwds=None, requestID=None,
      callback=None):
        """A work request consists of the a callable to be executed by a
        worker thread, a list of positional arguments, a dictionary
        of keyword arguments.

        A callback function can be specified, that is called when the results
        of the request are picked up from the result queue. It must accept
        two arguments, the request object and it's results in that order.
        If you want to pass additional information to the callback, just stick
        it on the request object.

        requestID, if given, must be hashable as it is used by the ThreadPool
        class to store the results of that work request in a dictionary.
        It defaults to the return value of id(self).
        """
        if requestID is None:
            self.requestID = id(self)
        else:
            self.requestID = requestID
        self.callback = callback
        self.callable = callable
        self.args = args or []
        self.kwds = kwds or {}


class ThreadPool:
    """A thread pool, distributing work requests and collecting results.

    See the module doctring for more information.
    """

    def __init__(self, num_workers, q_size=0):
        """Set up the thread pool and start num_workers worker threads.

        num_workers is the number of worker threads to start initialy.
        If q_size > 0 the size of the work request is limited and the
        thread pool blocks when queue is full and it tries to put more
        work requests in it.
        """

        self.requestsQueue = Queue.Queue(q_size)
        self.resultsQueue = Queue.Queue()
        self.workers = []
        self.workRequests = {}
        self.createWorkers(num_workers)

    def createWorkers(self, num_workers):
        """Add num_workers worker threads to the pool."""

        for i in range(num_workers):
            self.workers.append(WorkerThread(self.requestsQueue,
              self.resultsQueue))

    def dismissWorkers(self, num_workers):
        """Tell num_workers worker threads to to quit when they're done."""

        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()

    def putRequest(self, request):
        """Put work request into work queue and save for later."""

        self.requestsQueue.put(request)
        self.workRequests[request.requestID] = request

    def poll(self, block=False):
        """Process any new results in the queue."""
        while 1:
            try:
                # still results pending?
                if not self.workRequests:
                    raise NoResultsPending
                # are there still workers to process remaining requests?
                elif block and not self.workers:
                    raise NoWorkersAvailable
                # get back next results
                request, result = self.resultsQueue.get(block=block)
                # and hand them to the callback, if any
                if request.callback:
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Queue.Empty:
                break

    def wait(self):
        """Wait for results, blocking until all have arrived."""

        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break

def makeRequests(callable, args_list, callback=None):
    """Convenience function for building several work requests for the same
    callable with different arguments for each call.

    args_list contains the parameters for each invocation of callable.
    Each item in 'argslist' should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    callback is called when the results arrive in the result queue.
    """

    requests = []
    for item in args_list:
        if item == isinstance(item, tuple):
            requests.append(
              WorkRequest(callable, item[0], item[1], callback=callback))
        else:
            requests.append(
              WorkRequest(callable, [item], None, callback=callback))
    return requests


################
# USAGE EXAMPLE
################

if __name__ == '__main__':
    import random
    import time

    # the work the threads will have to do (rather trivial in our example)
    def do_something(data):
        time.sleep(random.randint(1,5))
        return round(random.random() * data, 5)

    # this will be called each time a result is available
    def print_result(request, result):
        print "Result: %s from request #%s" % (result, request.requestID)

    # assemble the arguments for each job to a list...
    data = [random.randint(1,10) for i in range(20)]
    # ... and build a WorkRequest object for each item in data
    requests = makeRequests(do_something, data, print_result)

    # we create a pool of 10 worker threads
    main = ThreadPool(3)

    # then we put the work requests in the queue...
    for req in requests:
        main.putRequest(req)
        print "Work request #%s added." % req.requestID
    # or shorter:
    # [main.putRequest(req) for req in requests]

    # ...and wait for the results to arrive in the result queue
    # wait() will return when results for all work requests have arrived
    # main.wait()

    # alternatively poll for results while doing something else:
    i = 0
    while 1:
        try:
            main.poll()
            print "Main thread working..."
            time.sleep(0.5)
            if i == 10:
                print "Adding 3 more worker threads..."
                main.createWorkers(3)
            i += 1
        except (KeyboardInterrupt, NoResultsPending):
            break
