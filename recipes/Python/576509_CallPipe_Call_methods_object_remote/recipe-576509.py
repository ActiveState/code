#  @brief An IPC channel allowing to call methods of an object from a
#  remote process. It is based on python's multiprocessing pipes:
#  instead of sending data, we send method call requests to an object
#  and transmit back the results (or exceptions). Works between
#  processes created by fork() (eg. multiprocessing.Process::start()).
#
# A CallPipe is bound to a 'target' object, and is made of 2 endpoints
# and one multiprocessing.Pipe inbetween:
# - a CallPipe_Callee, which is basically a thread listening to method
#   call requests coming on the pipe, calling the method on the target
#   object and returning the result onto the pipe to the caller
# - a CallPipe_Caller, which is a proxy object transforming the calls
#   to its __getattr__ into a MethodProxy object which in turns
#   transforms the calls to its __call__ method into request/response on
#   the pipe.
#
# A callpipe is associated with 1 'target' object, and should be used
# by 2 different processes: the one that contains the object, and the
# one that remotely calls the methods of the object. If there are more
# processes that have to call the methods on the target object, more
# callpipes have to be created (associated with the same target
# object).
#
# On the 'target' object side (CallPipe_Callee), each callpipe
# corresponds to a thread that may call its methods. As a consequence,
# the methods that might be called from the callpipe threads have to be
# thread-safe.
#
# On the remote side, the callpipe is multithread-safe. Currently, the
# implementation is very crude: only one remote thread is allowed to
# call a method from the target object at any given time (mutual
# exclusion).
#
# Note: Once the remote processes have a reference to the
# CallPipe_Caller object, they can discard any reference to the real
# object that might still exist in their image (due to the fork()
# nature of multiprocessing.Process::start()). In any case, if they
# call the methods of the (copy they have of the) target object,
# instead of the methods of the proxy, then they will act on their
# private copy of the object, not on the remote target object.

import threading, thread, os, select

try:
    # Tested with python 2.6 b3
    import multiprocessing
except ImportError:
    # Tested with standalone processing 0.52
    import processing as multiprocessing


class CallPipe_MethodProxy:
    """The remote proxy whose __call__ method sends the request and
    waits for the answer on the pipe"""
    def __init__(self, callpipe_caller, attr_name, cb_unregister = None):
        self.__caller     = callpipe_caller
        self.__attr_name  = attr_name
        self.__unregister = cb_unregister

    def __call__(self, *args, **kw):
        # We need to acquire the lock because if 2 threads concurrently
        # try to send/recv concurrently on the same pipe, the callee
        # will not be able to tell who is calling what and who it needs to
        # answer to.
        self.__caller._lock.acquire()
        try:
            self.__caller._endpoint.send((self.__attr_name, args, kw))
            recvdata = self.__caller._endpoint.recv()
        finally:
            self.__caller._lock.release()

        if len(recvdata) != 2:
            self.__caller._unregister(self.__attr_name)
            raise AttributeError(self.__attr_name)

        status, r = recvdata
        if status != "OK":
            raise r
        return r


class CallPipe_CallerProxy:
    """The remote proxy whose __getattr__ method simply calls
    CallPipe_Caller::get_method_proxy()"""
    def __init__(self, gateway):
        self.__gateway = gateway

    def __getattr__(self, attr_name):
        return self.__gateway._get_method_proxy(attr_name)


class CallPipe_Caller:
    """The callpipe endpoint which binds a CallPipe_CallerProxy to a
    request/response session over a pipe"""
    def __init__(self, endpoint):
        """Endpoint is an endpoint of a bidirectional multiprocessing.Pipe"""
        self._endpoint        = endpoint
        self._lock            = threading.Lock()
        self.__method_proxies = dict() # Cache of MethodProxy objects
        self.__proxy          = CallPipe_CallerProxy(self)

    def get_proxy(self):
        """Returns the associated CallPipe_CallerProxy object"""
        return self.__proxy

    def _get_method_proxy(self, method_name):
        """Called by the proxy object: creates a CallPipe_MethodProxy
        object for the given method name and store it into the local
        cache (__method_proxies). Returns the MethodProxy object."""
        self._lock.acquire()
        try:
            method_proxy = self.__method_proxies[method_name]
        except KeyError:
            method_proxy = CallPipe_MethodProxy(self, method_name)
            self.__method_proxies[method_name] = method_proxy
        finally:
            self._lock.release()
        return method_proxy

    def start(self):
        pass

    def stop(self):
        """Send a termination request to the CallPipe_Callee"""
        self.__endpoint.send(("TERMINATE",))
        self.__endpoint.close()

    def _unregister(self, attr_name):
        """Called by the CallPipe_MethodProxy object when the remote
        object signals an AttributeError, to remove it from the
        __method_proxies cache"""
        del self.__method_proxies[attr_name]


class CallPipe_CalleeThread(threading.Thread):
    """The thread that waits for the remote requests coming from the
    CallPipe_Caller at the other end of the pipe and performes the
    requested local method calls on the target object"""
    def __init__(self, termfd, endpoint, obj):
        """
        \param termfd is a file descriptor on which to select() to
        wait for termination requests from the main CallPipe_Callee
        thread
        \param Endpoint is an endpoint of a bidirectional multiprocessing.Pipe
        \param obj is the object on which to perform the method calls
        """
        threading.Thread.__init__(self)
        self.__endpoint = endpoint
        self.__obj      = obj
        self.__waitset  = select.poll()
        eventmask = select.POLLIN | select.POLLERR \
                    | select.POLLHUP | select.POLLPRI
        self.__waitset.register(self.__endpoint.fileno(), eventmask)
        self.__waitset.register(termfd, eventmask)

    def run(self):
        while True:
            # Check whether we received something from either the
            # callpipe or the terminating pipe
            fds = set([fd for fd, evt in self.__waitset.poll()])
            if len(fds) > 1:
                break
            if self.__endpoint.fileno() not in fds:
                break

            request = self.__endpoint.recv()
            if not isinstance(request, tuple) or len(request) != 3:
                # We have a problem. stopping ourselves
                try:
                    if request[0] == "TERMINATE":
                        raise SystemExit("Received a termination request.")
                except IndexError:
                    pass
                raise SystemExit("Invalid requests received by Callee.")

            method_name, args, kw = request
            try:
                method = None
                try:
                    method = getattr(self.__obj, method_name)
                except AttributeError:
                    self.__endpoint.send(("ATTRIBUTE_ERROR",))
                if method:
                    result = method(*args, **kw)
                    self.__endpoint.send(("OK", result))
            except Exception, ex:
                self.__endpoint.send(("EXCEPTION", ex))
            except:
                self.__endpoint.send(("EXCEPTION",
                                      RuntimeError("Uncaught exception")))

        # Closing the endpoint (never reached)
        self.__endpoint.close()


class CallPipe_Callee:
    """The object that binds the local target object to a thread
    listening for the method requests coming from the pipe"""
    def __init__(self, endpoint, obj):
        """
        \param Endpoint is an endpoint of a bidirectional multiprocessing.Pipe
        \param obj is the object on which to perform the method calls
        """
        term_r, term_w  = os.pipe()
        self.__obj      = obj
        self.__termpipe = term_w
        self.__thread   = CallPipe_CalleeThread(term_r, endpoint, obj)

    def get_object(self):
        return self.__obj

    def get_request_handler(self):
        return self.__thread

    def start(self):
        self.__thread.start()

    def stop(self):
        """Stop the thread performing the requests. Returns when the
        thread has been stopped"""
        # Send a terminate request to the terminating pipe.
        # Has to be called from outside the thread (otherwise: deadlock)
        os.write(self.__termpipe, "TERMINATE")
        self.__thread.join()


def CallPipe(obj):
    """
    Returns the endpoints of the callpipe:

    result[0]: a CallPipe_Callee object, the local endpoint referencing
               the target object (listening for requests)

    result[1]: a CallPipe_Caller object, the endpoint to remotely call
               the methods on the target object (sending requests)
    """
    src, dst = multiprocessing.Pipe()
    return (CallPipe_Callee(dst, obj), CallPipe_Caller(src))


if __name__ == "__main__":
    import time

    class MyObject:
        def __init__(self, name):
            self.__name  = name
            self.__trace = []
            self.__lock  = threading.Lock()

        def add_trace(self, item):
            self.__lock.acquire()
            try:
                self.__trace.append(item)
            finally:
                self.__lock.release()

        def get_traces(self):
            self.__lock.acquire()
            try:
                return self.__trace
            finally:
                self.__lock.release()

        def raise_exception(self):
            return 1/0

    class Process1(multiprocessing.Process):
        def __init__(self, obj_proxy):
            multiprocessing.Process.__init__(self)
            self.__obj = obj_proxy

        def run(self):
            for i in xrange(10):
                print "[%d] Calling add_trace %d..." % (os.getpid(), i)
                self.__obj.add_trace("I am pid %d in loop %d" % (os.getpid(),
                                                                 i))
                time.sleep(1)

            print "[%d] Now trying to get an exception..." % os.getpid()
            try:
                self.__obj.raise_exception()
            except ZeroDivisionError, ex:
                self.__obj.add_trace('I am pid %d and got the expected exception "%s".' % (os.getpid(), ex))
            finally:
                print "[%d] Exception test executed." % os.getpid()
            print "[%d] End of process." % os.getpid()

    class Process2(multiprocessing.Process):
        def __init__(self, obj_proxy):
            multiprocessing.Process.__init__(self)
            self.__obj = obj_proxy

        def run(self):
            for i in xrange(10):
                print "[%d] Calling add_trace %d..." % (os.getpid(), i)
                self.__obj.add_trace("I am pid %d in loop %d" % (os.getpid(),
                                                                 i))
                print "[%d] Calling get_traces %d..." % (os.getpid(), i)
                self.__obj.add_trace("I am pid %d and see %d traces before."\
                                     % (os.getpid(),
                                        len(self.__obj.get_traces())))
                time.sleep(1)

            print "[%d] Pausing 3 seconds..." % os.getpid()
            time.sleep(3)
            print "[%d] Calling final get_traces:" % os.getpid()
            for t in self.__obj.get_traces():
                print "[%d]   Trace: '%s'" % (os.getpid(), t)
            print "[%d] End of process." % os.getpid()

    # Creating object called by everybody
    obj = MyObject("The object")
    obj.add_trace("[%d] I am the parent of everything." % os.getpid())

    # Creating the callpipes
    print "[%d] Creating callpipes and processes..." % os.getpid()
    callpipe1 = CallPipe(obj)
    callpipe2 = CallPipe(obj)
    p1 = Process1(callpipe1[1].get_proxy())
    p2 = Process2(callpipe2[1].get_proxy())

    #
    # The next 2 steps can be done in any order
    #

    # Starting the children processes
    print "Starting children processes..."
    p1.start()
    p2.start()

    # Starting the callpipe threads
    print "Starting callpipes..."
    callpipe1[0].start()
    callpipe2[0].start()

    #
    # The previous 2 steps could be done in any order
    #

    # Waiting for children processes to finish
    print "Waiting for processes to terminate..."
    try:
        for p in p1,p2:
            p.join()
    except KeyboardInterrupt:
        for p in p1,p2:
            p.terminate()

    print "Processes terminated. Cleaning up..."
    obj.add_trace("[%d] I am the parent, and my children are done." \
                  % os.getpid())

    # Stopping the call pipe threads
    callpipe1[0].stop()
    callpipe2[0].stop()

    # Dump the contents of the object
    print "[%d] Children done. Dumping object:" % os.getpid()
    for t in obj.get_traces():
        print "  Trace: '%s'" % t
    print "Bye."
