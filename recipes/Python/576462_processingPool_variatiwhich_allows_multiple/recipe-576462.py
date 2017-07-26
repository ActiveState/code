## @brief A simple variant of processing.Pool that accepts requests
#  from different threads.


# Import 'multiprocessing' package (formerly known as 'processing'):
try:
    # Tested with python 2.6 b3
    from multiprocessing import Pool
except ImportError:
    # Tested with standalone processing 0.52
    from processing import Pool

import threading, sys


class MultiThreadedPool:
    """
    A simple variant of processing.Pool that accepts requests
    from different threads: makes sure that requests being processed by
    the worker processes are not redundant.

    When a thread B submits a request which is already being processed
    in the background for another thread A, then B doesn't re-submit the
    request: it waits for the same result object as A.

    This package makes the following asumption:
    - the result of the function to call is entirely determined by its
      arguments (resp. "function", "params")

    As a consequence, in order to determine whether a "request" has
    already been submitted by another thread, we ONLY compare the
    couples (function, params). If a submitted request has the same
    couple (function, params) as a request in progress, then we wait
    for this request to be completed (valid result, or exception)

    This Pool should be safe wrt exceptions in the remote function.
    Only the map() and imap() methods are implemented.
    """
    __lock      = None # threading.Lock object
    __inflight  = None # dict: (function, params) -> processing.ApplyResult obj
    __workers   = None # processing.Pool object

    def __init__(self, processes=None, initializer=None, initargs=()):
        """See processing.Pool.__init__()"""
        self.__workers  = Pool(processes, initializer, initargs)
        self.__inflight = dict()
        self.__lock     = threading.Lock()

        # Apply locking decorator on close/terminate/join
        self._unregister_jobs = self.__make_synchronized(self._unregister_jobs)
        self.close     = self.__make_synchronized(self.__workers.close)
        self.terminate = self.__make_synchronized(self.__workers.terminate)
        self.join      = self.__make_synchronized(self.__workers.join)

    def apply(self, func, args=()):
        """Equivalent to processing.Pool::apply(), but without the kwds{}
        argument"""
        self.__lock.acquire()
        try:
            key, job, i_am_owner = self._apply_async(func, args)
        finally:
            self.__lock.release()

        # Wait for result
        try:
            return job.get()
        finally:
            self._unregister_jobs([(key, job, i_am_owner)])

    def imap(self, func, iterable):
        """Equivalent to processing.Pool.imap(), but without the
        "chunksize" argument"""
        jobs = [] # list of tuples (key, result_object, bool_i_started_the_job)
        # Build the list of jobs started in the background
        self.__lock.acquire()
        try:
            for param in iterable:
                jobs.append(self._apply_async(func, (param,)))
        finally:
            self.__lock.release()

        # Wait for everybody
        try:
            for key, job, i_am_owner in jobs:
                yield job.get()
        finally:
            self._unregister_jobs(jobs)

    def map(self, func, iterable):
        """Equivalent to processing.Pool.map(), but without the
        "chunksize" argument"""
        return list(self.imap(func, iterable))

    def _apply_async(self, func, args):
        """Return a tuple (inflight_key, applyResult object, i_am_owner)"""
        key = (func, args)
        try:
            # Job already started by somebody else
            job = self.__inflight[key]
            return key, job, False
        except KeyError:
            # We have to start a new job
            job = self.__workers.apply_async(func, args)
            self.__inflight[key] = job
            return key, job, True

    def _unregister_jobs(self, jobs):
        """
        Remove all the given "in flight" jobs.
        Due to a limitation of processing 0.52, we have to wake up
        additional threads waiting for the result by hand. The correct
        fix to processing would be to replace self._cond.notify() in
        ApplyResult::set() by self._cond.notifyAll()
        """
        for key, job, i_am_owner in jobs:
            # Begin workaround
            # processing.ApplyResult._set doesn't call notifyAll !
            # we have to do it ourselves.
            # Don't move it: nothing guarantees
            # that the owner will be the 1st to wake up !
            job._cond.acquire()
            job._cond.notifyAll()
            job._cond.release()
            # End workaround

            if not i_am_owner:
                # Don't remove it from the in_flight list
                continue
            try:
                del self.__inflight[key]
            except KeyError:
                print >>sys.stderr, "Warning: job not in queue", key, job

    def __make_synchronized(self, f):
        """Local decorator to make a method calling lock acquire/release"""
        def newf(*args, **kw):
            self.__lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                self.__lock.release()
        return newf


if __name__ == "__main__":
    import os, time

    def f(params):
        delay, msg = params
        print "Calling sleep(%f) in %d with msg '%s'" % (delay,
                                                         os.getpid(), msg)
        time.sleep(delay)
        print "End of sleep(%f) in %d with msg '%s'" % (delay,
                                                        os.getpid(), msg)
        return "Slept %fs" % delay


    # We have to create the Pool AFTER the functions to call in it have been
    # defined. Using 3 worker processes
    pool = MultiThreadedPool(3)

    # Small test for apply() first
    print pool.apply(f, ((1.2, "Sleep 1200ms to test apply()"),))

    # Now test map()...
    class TestThread(threading.Thread):
        def __init__(self, params):
            threading.Thread.__init__(self)
            self.__params = params

        def run(self):
            print "Running on", self.__params
            try:
                r = pool.map(f, self.__params)
                print "Got result:", r
            except:
                print "Got exception", sys.exc_info()[0:2]

    jobs = ((1, "Sleep 1s"), (2, "Sleep 2s"), (3, "Sleep 3s"),
            (2.5, "BisSleep 2.5s"))
    # Jobs that will execute the same parallel tasks
    # Note: total duration = 3.5s because we have a pool of 3 processes
    t1 = TestThread(list(jobs))
    t2 = TestThread(list(jobs))
    t3 = TestThread(list(jobs))
    t4 = TestThread(list(jobs))
    t5 = TestThread(list(jobs))

    # jobs with a failure
    jobs = jobs + ((-42, "Invalid negative sleep time"),)
    tfail1 = TestThread(list(jobs))
    tfail2 = TestThread(list(jobs))

    # Starting 1st thread
    t1.start()

    time.sleep(1.5)
    # Starting a 2nd thread, which is asking for the same data t1 is
    # already processing
    t2.start()
    time.sleep(.5)
    t3.start()
    t4.start()
    # Should return at the same time as t1, with the same results

    # Wait for all of them to complete
    time.sleep(4)
    print "### We should start all over again now..."
    t5.start()
    # Starting 2 threads which should fail with an exception
    time.sleep(1)
    tfail1.start()
    tfail2.start()
    # 1 Thread should have finished, the 2 others
    # returned en exception almost at the same time
