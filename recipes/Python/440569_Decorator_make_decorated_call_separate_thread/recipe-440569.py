#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
################################################################################
#
# Decorator @threadmethod(sec), makes decorated method calls to always 
# execute in a separate new thread with a specified timeout, propagating 
# exceptions, as well as a result. 
# Dmitry Dvoinikov <dmitry@targeted.org>
#
# from threadmethod import *
#
# class NetworkedSomething(object):
#     @threadmethod(10.0)
#     def connect(self, host, port):
#         ... this could take long long time ...
#    
# # the following call throws ThreadMethodTimeoutError upon a 10 sec. timeout
# NetworkedSomething().connect("123.45.67.89", 1234). Similarly, 
#
# @threadmethod()
# def foo():
#     ...
#
# makes foo() an async method, which just executes in a new separate thread
# each time, but that thread is not waited for, it's just launched to execute 
# in parallel. Besides, in the latter case foo() returns a reference to the
# created thread, so that it can be join()ed.
#
################################################################################

__all__ = [ "threadmethod", "ThreadMethodTimeoutError" ]

################################################################################

class ThreadMethodTimeoutError(Exception): pass

################################################################################

from threading import Thread

class ThreadMethodThread(Thread):
    "ThreadMethodThread, daemonic descendant class of threading.Thread which " \
    "simply runs the specified target method with the specified arguments."

    def __init__(self, target, args, kwargs):
        Thread.__init__(self)
        self.setDaemon(True)
        self.target, self.args, self.kwargs = target, args, kwargs
        self.start()

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception, e:
            self.exception = e
        except:
            self.exception = Exception()
        else:
            self.exception = None

################################################################################

def threadmethod(timeout = None):
    "@threadmethod(timeout), decorator function, returns a method wrapper " \
    "which runs the wrapped method in a separate new thread."

    def threadmethod_proxy(method):
    
        if hasattr(method, "__name__"):
            method_name = method.__name__
        else:
            method_name = "unknown"

        def threadmethod_invocation_proxy(*args, **kwargs):
            worker = ThreadMethodThread(method, args, kwargs)
            if timeout is None:
                return worker
            worker.join(timeout)
            if worker.isAlive():
                raise ThreadMethodTimeoutError("A call to %s() has timed out" 
                                               % method_name)
            elif worker.exception is not None:
                raise worker.exception
            else:
                return worker.result

        threadmethod_invocation_proxy.__name__ = method_name

        return threadmethod_invocation_proxy

    return threadmethod_proxy

################################################################################

if __name__ == "__main__": # run self-tests

    print "self-testing module threadmethod.py:"

    from threading import currentThread

    mainthread = currentThread()
    @threadmethod(5)
    def tryme():
        assert currentThread() is not mainthread
    tryme()

    @threadmethod(5)
    def foo(a, b, c):
        return a + b + c
    assert foo(1, 2, 3) == 6

    @threadmethod(5)
    def foo(*args):
        assert args == ("foo", )
        return args[0]
    assert foo("foo") == "foo"

    @threadmethod(5)
    def foo(**kwargs):
        assert kwargs == { "foo" : "bar" }
        return kwargs["foo"]
    assert foo(foo = "bar") == "bar"

    @threadmethod(5)
    def foo(a, b, *args, **kwargs):
        assert a == 1 and b == "foo" and args == ("bar", ) and kwargs == { "biz" : "baz" }
    assert foo(1, "foo", "bar", biz = "baz") is None

    from time import sleep
    
    class bar(object):
        @threadmethod(3)
        def __init__(self, timeout):
            sleep(timeout)
        @threadmethod(1)
        def throw(self, e):
            raise e

    try:
        bar(5)
    except ThreadMethodTimeoutError:
        pass
    else:
        assert False, "Constructor should have timed out"

    try:
        bar(1).throw(IOError("fatal"))
    except IOError, e:
        assert str(e) == "fatal"
    else:
        assert False, "Expected IOError(\"fatal\")"

    x = 0

    @threadmethod()
    def async():
        global x
        sleep(0.25)
        x += 1

    async()

    while x == 0:
        pass

    @threadmethod()
    def foo():
        sleep(1.0)
        
    foo().join()

    print "ok"

################################################################################
