"""
An ActiveObject forward messages to an internal passive object
running on its own thread.

The passive object processes these messages sequentially, and returns the results
or any exceptions to the caller via an AsyncResult object.
"""

from threading import Thread, Event, RLock

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


class AsyncResult:
    """Represents an asynchronous operation that may not have completed yet."""

    def __init__(self):
        self.__completed = False
        self.__failed = False
        self.__wait = Event()
        self.__callbacks = []
        self.__errbacks = []
        self.__retval = None
        self.__error = None
        self.__lock = RLock()

    def complete(self):
        with self.__lock:
            self.__completed = True
            self.__wait.set()

    def succeed(self, retval):
        self.__retval = retval
        self.complete()
        for callback in self.__callbacks:
            callback(retval)
        self.clear_callbacks()

    def fail(self, error):
        self.__error = error
        self.__failed = True
        self.complete()
        for errback in self.__errbacks:
            errback(error)
        self.clear_callbacks()

    def clear_callbacks(self):
        self.__callbacks = []
        self.__errbacks = []

    def add_callback(self, callback, errback=None):
        with self.__lock:
            if self.__completed:
                if not self.__failed:
                    callback(self.__retval)
            else:
                self.__callbacks.append(callback)
            if errback:
                self.add_errback(errback)

    def add_errback(self, errback):
        with self.__lock:
            if self.__completed:
                if self.__failed:
                    errback(self.__error)
            else:
                self.__errbacks.append(errback)

    @property
    def result(self):
        self.__wait.wait()
        if not self.__failed:
            return self.__retval
        else:
            raise self.__error


class Message:
    """Represents a message forwarded to a passive object by an active object"""

    def __init__(self, fun, queue):
        self.fun = fun
        self.queue = queue

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.result = AsyncResult()
        self.queue.put(self)
        return self.result

    def call(self):
        return self.fun(*self.args, **self.kwargs)


class ActiveObject:
    """An object that handles messages sequentially on a separate thread.
    Call stop() to terminate the object's internal message loop."""

    def __init__(self, klass, *args, **kwargs):
        self.__obj = klass(*args, **kwargs)
        self.__queue = Queue()
        self.__thread = Thread(target=self.__process_queue)
        self.__thread.start()
        self.stopped = False

    def stop(self):
        self.__queue.put(StopIteration)

    def __process_queue(self):
        while True:
            message = self.__queue.get()
            retval = None
            failure = None
            if message == StopIteration:
                self.stopped = True
                break
            try:
                retval = message.call()
            except Exception as e:
                failure = e
            if failure is None:
                message.result.succeed(retval)
            else:
                message.result.fail(failure)

    def __getattr__(self, attrname):
        if self.stopped:
            raise AttributeError("Object is no longer active.")
        fun = getattr(self.__obj, attrname)
        if callable(fun):
            return Message(getattr(self.__obj, attrname), self.__queue)
        else:
            raise AttributeError("Active object does not support this function.")
