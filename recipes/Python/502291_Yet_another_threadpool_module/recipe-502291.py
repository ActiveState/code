'''
Yet another thread pool module.

A thread pool consists of a set of worker threads for performing time consuming
operations concurrently. A minimal API provides a way to submit jobs (requests),
without waiting for them to finish, and get the results back in some way once
they are available. The thread pool is responsible for assigning jobs to the
worker threads by putting them in a job queue, where they are picked up by the
next available worker. The worker then performs the assigned job in the background
and puts the processed request in an output queue.

The main novelty of this module compared to other threadpool recipes is the way
results are returned to the client. Instead of providing a callback to post-process
the computed results, a L{generator <ThreadPool.iterProcessedJobs>} is used for
popping the processed jobs from the output queue and yielding them back to the
caller. The processed jobs encapsulate the computed result (or raised exception)
and can be used transparently by the calling thread, as if the computation didn't
take place in a different thread. This is more flexible that the callback-based
approach since it gives full control to the caller of when to ask for a result,
how long to wait for it and what to do with it once it is fetched.

After a C{JobRequest} is L{added <ThreadPool.addJob>} to a L{ThreadPool}, it can
be in one of the following states:
    1. Unassigned: The request is still in the input queue, no worker thread
    has been assigned to it yet. There are two substates:
        - Pending: The job is waiting its turn to be picked up by a L{Worker}.
        - Cancelled: The job has been L{cancelled <ThreadPool.cancelJob>} and,
          although it still occupies a slot in the input queue, it will be
          discarded when a L{Worker} picks it up.
    2. In progress: The job has been popped by the input queue by a L{Worker} and
       is in the process of being executed.
    3. Processed: The job has been processed (successfully or not) and has been
       added to the output queue, ready to be returned.
    4. Returned: The job has been returned to the client, either by
       L{ThreadPool.iterProcessedJobs} or L{ThreadPool.processedJobs} and is no
       longer associated with the threadpool.
A job in state 1.a, 2 or 3 is said to be I{active}.

B{Acknowledgements:} The basic concept and the initial implementation was taken
from the U{threadpool module of Christopher Arndt
<http://www.chrisarndt.de/en/software/python/threadpool/>}, who in turn borrowed
from the "Python in a Nutshell" book by Alex Martelli.
'''

__all__ = ['ThreadPool', 'JobRequest']
__author__ = 'George Sakkis'

import sys
import time
import Queue
import logging
import threading

_log = logging.getLogger('threadpool')


def synchronized(f):
    '''A synchronized method decorator'''
    def wrapper(self, *args, **kwargs):
        try: lock = self.__lock
        except AttributeError: # first time use
            lock = self.__dict__.setdefault('__lock', threading.RLock())
        lock.acquire()
        try: return f(self, *args, **kwargs)
        finally: lock.release()
    return wrapper


class ThreadPool(object):
    '''A thread pool, distributing job requests and collecting them after they
    are processed.

    See the module doctring for more information.
    '''

    def __init__(self, num_workers, input_queue_size=0, output_queue_size=0):
        '''Set up the thread pool and start C{num_workers} worker threads.

        @param num_workers: The number of worker threads to start initially.
        @param input_queue_size: If a positive integer, it's the maximum number
            of unassigned jobs. The thread pool blocks when the queue is full a
            new job is submitted.
        @param output_queue_size: If a positive integer, it's the maximum number
            of completed jobs waiting to be fetched. The thread pool blocks when
            the queue is full and a job is completed.
        '''
        self._workers = []
        self._activeKey2Job = {}
        self._unassignedKey2Job = {}
        self._unassignedJobs = Queue.Queue(input_queue_size)
        self._processedJobs = Queue.Queue(output_queue_size)
        self.addWorkers(num_workers)

    @synchronized
    def addWorkers(self, n=1):
        '''Add C{n} worker threads to the pool.'''
        for _ in xrange(n):
            self._workers.append(Worker(self._unassignedJobs, self._processedJobs,
                                        self._unassignedKey2Job))
        _log.debug('Added %d workers' % n)

    @synchronized
    def dismissWorkers(self, n=1):
        'Tell C{n} worker threads to quit after they finish with their current job.'
        for _ in xrange(n):
            try: self._workers.pop().dismissed = True
            except KeyError: break

    @synchronized
    def addJob(self, job, timeout=None):
        '''Add a job request to the end of the input queue.

        @param timeout: If the input queue is full and C{timeout is None}, block
            until a slot becomes available. If C{timeout > 0}, block for up to
            C{timeout} seconds and raise C{Queue.Full} exception if the queue is
            still full. If C{timeout <= 0}, do not block and raise C{Queue.Full}
            immediately if the queue is full.
        '''
        key = job.key
        self._unassignedJobs.put(job, timeout is None or timeout>0, timeout)
        self._unassignedKey2Job[key] = self._activeKey2Job[key] = job
        _log.debug('Added job %r to the input queue' % key)

    @synchronized
    def cancelJob(self, key):
        '''Cancel a job.

        This has effect only if the job is still unassigned; if it's in progress
        or has already been processed, it has no effect.

        @param key: The job's identifier.
        '''
        try:
            del self._unassignedKey2Job[key]
            # if it's not in unassigned, it may be in progress or already
            # processed; don't try to delete it from active
            del self._activeKey2Job[key]
        except KeyError: pass

    @synchronized
    def cancelAllJobs(self):
        '''Cancel all unassigned jobs.'''
        while self._unassignedKey2Job:
            del self._activeKey2Job[self._unassignedKey2Job.popitem()[0]]

    def numActiveJobs(self):
        '''Return the approximate number of active jobs.

        This is not reliable due to thread semantics.
        '''
        return len(self._activeKey2Job)

    def iterProcessedJobs(self, timeout=None):
        '''Return an iterator over processed job requests, popping them off the
        output queue.

        @param timeout: There are three cases:
            - If C{None}, iterate over the processed jobs as long as there are
            any active jobs. Whenever there are no processed jobs available,
            block and wait for a job to finish.
            - If C{<= 0}, iterate over the currently processed jobs only; do not
            block.
            - If C{> 0}, wait up to C{timeout} seconds per processed job as long
            as there are active jobs. Note that a loop such as::
                for r in t.iterProcessedJobs(2): pass
            may take from microseconds (if there are no active jobs) to
            arbitrarily long time, as long as each processed job is yielded
            within 2 seconds. If you want a timeout for the whole loop, use
            L{processedJobs} instead.
        '''
        block = timeout is None or timeout>0
        while self._activeKey2Job:
            try: job = self._processedJobs.get(block, timeout)
            except Queue.Empty:
                break
            key = job.key
            _log.debug('Popped job %r from the output queue' % key)
            # at this point the key is guaranteed to be in _activeKey2Job even
            # if the job has been cancelled
            assert key in self._activeKey2Job
            del self._activeKey2Job[key]
            yield job

    def processedJobs(self, timeout=None):
        '''Return a list of processed job requests.

        @param timeout: If C{timeout is None} or C{timeout <= 0}, it is
            equivalent to C{list(t.iterProcessedJobs(timeout))}. If C{timeout > 0},
            this is the maximum overall time to spend on collecting processed jobs.
        '''
        if timeout is None or timeout <= 0:
            return list(self.iterProcessedJobs(timeout))
        now = time.time
        end = now() + timeout
        processed = []
        while timeout > 0:
            try: processed.append(self.iterProcessedJobs(timeout).next())
            except StopIteration: break
            timeout = end - now()
        return processed


class JobRequest(object):
    '''A request to execute a callable later and encapsulate its result or
    exception info.
    '''

    class UnprocessedRequestError(Exception):
        '''The callable of a L{JobRequest} has not been called yet.'''

    def __init__(self, callable, args=(), kwds=None, key=None):
        '''Create a job request for a callable.

        A job request consists of the a callable to be executed by a L{worker
        thread <Worker>}, a list of positional arguments and a dictionary of
        keyword arguments.

        @param key: If given, it must be hashable to be used as identifier of
            the request. It defaults to C{id(self)}.
        '''
        if kwds is None: kwds = {}
        if key is None: key = id(self)
        for attr in 'callable', 'args', 'kwds', 'key':
            setattr(self, attr, eval(attr))
        self._exc_info = None

    def process(self):
        '''Execute the callable of this request with the given arguments and
        store the result or the raised exception info.
        '''
        _log.debug('Ready to process job request %r' % self.key)
        try:
            self._result = self.callable(*self.args, **self.kwds)
        except:
            self._exc_info = sys.exc_info()
            _log.debug('Failed to process job request %r' % self.key)
        else:
            self._exc_info = None
            _log.debug('Job request %r was processed successfully' % self.key)

    def result(self):
        '''Return the computed result for this processed request.

        If the callable had risen an exception, it is reraised here with its
        original traceback.

        @raise JobRequest.UnprocessedRequestError: If L{process} has not been
            called for this request.
        '''
        if self._exc_info is not None:
            tp,exception,trace = self._exc_info
            raise tp,exception,trace
        try: return self._result
        except AttributeError:
            raise self.UnprocessedRequestError


class Worker(threading.Thread):
    '''Background thread connected to the input/output job request queues.

    A worker thread sits in the background and picks up job requests from one
    queue and puts the processed requests in another, until it is dismissed.
    '''

    def __init__(self, inputQueue, outputQueue, unassignedKey2Job, **kwds):
        '''Set up thread in daemonic mode and start it immediatedly.

        @param inputQueue, outputQueue: U{Queues
        <http://docs.python.org/lib/module-Queue.html>} passed by the L{ThreadPool}
        class when it creates a new worker thread.
        '''
        super(Worker,self).__init__(**kwds)
        self.setDaemon(True)
        self._inputQueue = inputQueue
        self._outputQueue = outputQueue
        self._unassignedKey2Job = unassignedKey2Job
        self.dismissed = False
        self.start()

    def run(self):
        '''Poll the input job queue indefinitely or until told to exit.

        Once a job request has been popped from the input queue, process it and
        add it to the output queue if it's not cancelled, otherwise discard it.
        '''
        while True:
            # thread blocks here if inputQueue is empty
            job = self._inputQueue.get()
            key = job.key
            _log.debug('Popped job request %r from the input queue' % key)
            try: del self._unassignedKey2Job[key]
            except KeyError:
                _log.info('Discarded cancelled job request %r' % key)
                continue
            if self.dismissed: # put back the job we just picked up and exit
                self._inputQueue.put(job)
                _log.debug('Dismissing worker %r' % self.getName())
                break
            job.process()
            # thread blocks here if outputQueue is full
            self._outputQueue.put(job)
            _log.debug('Added job request %r to the output queue' % job.key)


if __name__ == '__main__':
    # demo
    import random

    # change the seed to get different sequence of results
    random.seed(2)

    # the work the workers threads will have to do
    def slow_sqrt(num):
        t = random.randrange(1,5)
        log('%s: pretending to work hard on computing sqrt(%s) for %d seconds' %
            (threading.currentThread().getName(),num,t))
        time.sleep(t)
        return num**0.5

    # log each completed job
    def job_done(job):
        # job.result() will reraise any exception raised while the job was being
        # processed; otherwise it will return the computed result
        try:
            return 'job #%s: result=%s' % (job.key, job.result())
        except Exception, ex:
            return 'job #%s: exception raised: %s' % (job.key, ex)

    def log(msg, start=time.time()):
        print '%.2f seconds elapsed: %s' % (time.time()-start, msg)

    # create a pool of 3 worker threads
    pool = ThreadPool(3)

    # create 10 job requests and add them in the queue
    for i in xrange(10):
        num = random.randrange(-3,7)
        pool.addJob(JobRequest(slow_sqrt, [num]))

    # collect all processed jobs within 3.5 seconds
    firstbatch = pool.processedJobs(timeout=3.5)
    log('%d jobs done:' % len(firstbatch))
    for job in firstbatch:
        print '    ', job_done(job)
    print '** %d active jobs after first batch' % pool.numActiveJobs()

    # non-blocking iterator over processed jobs
    for i in xrange(5):
        for job in pool.iterProcessedJobs(timeout=0):
            log('From non-blocking loop: %s' % job_done(job))
        if pool.numActiveJobs():
            log('Do something in the main thread; will check the pool again after a sec')
            time.sleep(1)
    print '** %d active jobs after second batch' % pool.numActiveJobs()

    # blocking iterator over any remaining active jobs
    for job in pool.iterProcessedJobs():
        log('From blocking loop: %s' % job_done(job))
    print '** %d active jobs after third batch' % pool.numActiveJobs()
