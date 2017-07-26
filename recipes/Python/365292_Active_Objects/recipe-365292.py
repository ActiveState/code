"""
An ActiveObject forward messages to an internal passive object
running on its own thread.

The passive object processes these messages sequentially, and returns the results
or any exceptions to the caller via an AsyncResult object.
"""

from threading import Thread, Event, RLock
from Queue import Queue

class AsyncResult:
    """Represents an asynchronous operation that may not have completed yet."""
    def __init__(self):
        self.completed = False
        self.failed = False
        self.__wait = Event()
        self.__callbacks = []
        self.__errbacks = []
        self.__retval = None
        self.__error = None
        self.__lock = RLock()

    def complete(self):
        self.__lock.acquire()
        self.completed = True
        self.__wait.set()
        self.__lock.release()

    def succeed(self, retval):
        self.__retval = retval
        self.complete()
        for callback in self.__callbacks:
            callback(retval)
        self.clearCallbacks()
        
    def fail(self, error):
        self.__error = error
        self.failed = True
        self.complete()
        for errback in self.__errbacks:
            errback(error)
        self.clearCallbacks()

    def clearCallbacks(self):
        self.__callbacks = []
        self.__errbacks = []

    def addCallback(self, callback, errback=None):
        self.__lock.acquire()
        try:
            if self.completed:
                if not self.failed:
                    callback(self.__retval)
            else:
                self.__callbacks.append(callback)
            if not errback == None:
                self.addErrback(errback)
        finally:
            self.__lock.release()

    def addErrback(self, errback):
        self.__lock.acquire()
        try:
            if self.completed:
                if self.failed:
                    errback(self.__error)
            else:
                self.__errbacks.append(errback)
        finally:
            self.__lock.release()
            
    def __getResult(self):
        self.__wait.wait()
        if not self.failed:
            return self.__retval
        else:
            raise self.__error
    result=property(__getResult)

       
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
        return self.fun(*(self.args), **(self.kwargs))

class ActiveObject:
    """An object that handles messages sequentially on a separate thread.
    Call stop() to terminate the object's internal message loop."""
    def __init__(self, klass, *args, **kwargs):
        self.__obj = klass(*args, **kwargs)
        self.__queue = Queue()
        self.__thread = Thread(target=self.__processQueue)
        self.__thread.start()
        self.stopped = False

    def stop(self):
        self.__queue.put(StopIteration)
        
    def __processQueue(self):
        while True:
            message = self.__queue.get()
            retval = None
            failure = None
            if message==StopIteration:
                self.stopped = True
                break
            try:
                retval = message.call()
            except Exception, e:
                failure = e
            if failure==None:
                message.result.succeed(retval)
            else:
                message.result.fail(failure)
            
    def __getattr__(self, attrname):
        if self.stopped:
            raise AttributeError("Object is no longer active.")
        fun = getattr(self.__obj, attrname)
        if hasattr(fun, '__call__'):
            return Message(getattr(self.__obj, attrname), self.__queue)
        else:
            raise AttributeError("Active object does not support this function.")
