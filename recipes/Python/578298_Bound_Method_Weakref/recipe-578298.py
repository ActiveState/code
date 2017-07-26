import weakref


class _BoundMethodWeakref:
    def __init__(self, func):
        self.func_name = func.__name__
        self.wref = weakref.ref(func.__self__) #__self__ returns the class http://docs.python.org/reference/datamodel.html

    def __call__(self):
        func_cls = self.wref()
        if func_cls is None: #lost reference
            return None
        else:
            func = getattr(func_cls, self.func_name)
            return func

    #def __cmp__(self, other):
        #I decided to remove this, so it will behave the same as weakref.ref
        #func = self.__call__()
        #return cmp(func, other)

def weak_ref(callback):
    if hasattr(callback, '__self__') and callback.__self__ is not None: #is a bound method?
        return _BoundMethodWeakref(callback)
    else:
        return weakref.ref(callback)


if __name__ == "__main__":
    class Some:
        def __init__(self):
            pass
			
        def func(self):
            pass

    some = Some()
    some_func = some.func
    weak = weak_ref(some_func)
    some_list = [weak, ]
    if weak in some_list:
        print "yeah"
    print weak()
    del some
    del some_func
    print weak()
