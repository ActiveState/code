"""
History:
version 1.2:
- callables and non-callables have distinct classes, now.
- Added a simple factory function TProxy.
"""

#Import modules.
from thread import allocate_lock as Lock


class TObjectProxy(object):
    """The TObjectProxy class wrapper."""

    def __init__(self, obj, lock = None):
        """The initializer."""
        if lock is None:
            lock = Lock()
        super(TObjectProxy, self).__init__(obj, lock)
        #I'm paranoid => attributes are private.
        super(TObjectProxy, self).__setattr__('_TObjectProxy__obj', obj)
        super(TObjectProxy, self).__setattr__('_TObjectProxy__lock', lock)

    def __repr__(self):
        lock = super(TObjectProxy, self).__getattribute__('_TObjectProxy__lock')
        obj = super(TObjectProxy, self).__getattribute__('_TObjectProxy__obj')
        cls = super(TObjectProxy, self).__getattribute__('__class__')
        return "%s<%r, %r>" % (cls.__name__, obj, lock)

    #Every attribute get/set is wrapped between locks.
    def __getattribute__(self, name):
        lock = super(TObjectProxy, self).__getattribute__('_TObjectProxy__lock')
        #Marshall everything else to wrapped object
        obj = super(TObjectProxy, self).__getattribute__('_TObjectProxy__obj')
        lock.acquire()
        try:
            ret = TProxy(getattr(obj, name), lock)
        finally:
            lock.release()
        return ret

    def __setattr__(self, name, value):
        obj = super(TObjectProxy, self).__getattribute__('_TObjectProxy__obj')
        lock = super(TObjectProxy, self).__getattribute__('_TObjectProxy__lock')
        lock.acquire()
        try:
            setattr(obj, name, value)
        finally:
            lock.release()

    def __delattr__(self, name):
        obj = super(TObjectProxy, self).__getattribute__('_TObjectProxy__obj')
        lock = super(TObjectProxy, self).__getattribute__('_TObjectProxy__lock')
        lock.acquire()
        try:
            delattr(obj, name)
        finally:
            lock.release()


class TCallableProxy(TObjectProxy):
    """The TCallableProxy class wrapper."""

    def __init__(self, handler, lock = None):
        """The initializer."""
        if lock is None:
            lock = Lock()
        if callable(handler):
            super(TCallableProxy, self).__init__(handler, lock)
        else:
            raise TypeError("Object not callable.", handler)

    def __call__(self, *args, **kwargs):
        #Get obj and lock => Note how super call uses TObjectProxy.
        obj = super(TObjectProxy, self).__getattribute__('_TObjectProxy__obj')
        lock = super(TObjectProxy, self).__getattribute__('_TObjectProxy__lock')
        lock.acquire()
        try:
            ret = obj(*args, **kwargs)
        finally:
            lock.release()
        return ret


def TProxy(obj, lock = RLock()):
    """A factory function wrapping an object in a thread-safe wrapper."""
    if callable(obj):
        return TCallableProxy(obj, lock)
    else:
        return TObjectProxy(obj, lock)
