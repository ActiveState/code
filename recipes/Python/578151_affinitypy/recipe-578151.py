"""Allow a simple way to ensure execution is confined to one thread.

This module defines the Affinity data type that runs code on a single thread.
An instance of the class will execute functions only on the thread that made
the object in the first place. The class is useful in a GUI's main loop."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '4 June 2012'
__version__ = 1, 0, 0

################################################################################

import sys
import _thread
import queue

################################################################################

def slots(names=''):
    "Sets the __slots__ variable in the calling context with private names."
    sys._getframe(1).f_locals['__slots__'] = \
        tuple('__' + name for name in names.replace(',', ' ').split())

################################################################################

class Affinity:

    "Affinity() -> Affinity instance"

    slots('thread, action')

    def __init__(self):
        "Initializes instance with thread identity and job queue."
        self.__thread = _thread.get_ident()
        self.__action = queue.Queue()

    def __call__(self, func, *args, **kwargs):
        "Executes function on creating thread and returns result."
        if _thread.get_ident() == self.__thread:
            while not self.__action.empty():
                self.__action.get_nowait()()
            return func(*args, **kwargs)
        delegate = _Delegate(func, args, kwargs)
        self.__action.put_nowait(delegate)
        return delegate.value

################################################################################

class _Delegate:

    "_Delegate(func, args, kwargs) -> _Delegate instance"

    slots('func, args, kwargs, mutex, value, error')

    def __init__(self, func, args, kwargs):
        "Initializes instance from arguments and prepares to run."
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__mutex = _thread.allocate_lock()
        self.__mutex.acquire()

    def __call__(self):
        "Executes code with arguments and allows value retrieval."
        try:
            self.__value = self.__func(*self.__args, **self.__kwargs)
            self.__error = False
        except:
            self.__value = sys.exc_info()[1]
            self.__error = True
        self.__mutex.release()

    @property
    def value(self):
        "Waits for value availability and raises or returns data."
        self.__mutex.acquire()
        if self.__error:
            raise self.__value
        return self.__value
