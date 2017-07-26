# File weakmethod.py
from weakref import *

class _weak_callable:

    def __init__(self,obj,func):
        self._obj = obj
        self._meth = func

    def __call__(self,*args,**kws):
        if self._obj is not None:
            return self._meth(self._obj,*args,**kws)
        else:
            return self._meth(*args,**kws)

    def __getattr__(self,attr):
        if attr == 'im_self':
            return self._obj
        if attr == 'im_func':
            return self._meth
        raise AttributeError, attr

class WeakMethod:
    """ Wraps a function or, more importantly, a bound method, in
    a way that allows a bound method's object to be GC'd, while
    providing the same interface as a normal weak reference. """

    def __init__(self,fn):
        try:
            self._obj = ref(fn.im_self)
            self._meth = fn.im_func
        except AttributeError:
            # It's not a bound method.
            self._obj = None
            self._meth = fn

    def __call__(self):
        if self._dead(): return None
        return _weak_callable(self._obj(),self._meth)

    def _dead(self):
        return self._obj is not None and self._obj() is None
