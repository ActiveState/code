def _get_method_names (obj):
    from types import *
    if type(obj) == InstanceType:
        return _get_method_names(obj.__class__)
    
    elif type(obj) == ClassType:
        result = []
        for name, func in obj.__dict__.items():
            if type(func) == FunctionType:
                result.append((name, func))

        for base in obj.__bases__:
            result.extend(_get_method_names(base))

        return result


class _SynchronizedMethod:

    def __init__ (self, method, obj, lock):
        self.__method = method
        self.__obj = obj
        self.__lock = lock

    def __call__ (self, *args, **kwargs):
        self.__lock.acquire()
        try:
            return self.__method(self.__obj, *args, **kwargs)
        finally:
            self.__lock.release()


class SynchronizedObject:
    
    def __init__ (self, obj, ignore=[], lock=None):
        import threading

        self.__methods = {}
        self.__obj = obj
        lock = lock and lock or threading.RLock()
        for name, method in _get_method_names(obj):
            if not name in ignore:
                self.__methods[name] = _SynchronizedMethod(method, obj, lock)

    def __getattr__ (self, name):
        try:
            return self.__methods[name]
        except KeyError:
            return getattr(self.__obj, name)



if __name__ == '__main__':
    import threading
    import time

    class Dummy:

        def foo (self):
            print 'hello from foo'
            time.sleep(1)

        def bar (self):
            print 'hello from bar'

        def baaz (self):
            print 'hello from baaz'


    tw = SynchronizedObject(Dummy(), ['baaz'])
    threading.Thread(target=tw.foo).start()
    time.sleep(.1)
    threading.Thread(target=tw.bar).start()
    time.sleep(.1)
    threading.Thread(target=tw.baaz).start()


#hello from foo
#hello from baaz
#hello from bar   
