from threading import Thread
LARGE = 100000

class Future:
    def __init__(self, f):
        self.__f = f
        self.__thread = None
        self.__exception = None
        
    def __call__(self, *args, **kw):
        self.__thread = Thread(target=self.runfunc, args=args, kwargs=kw)
        self.__thread.start()
        return self
    
    def runfunc(self, *args, **kw):
        try:
            self.__val = self.__f(*args, **kw)
        except Exception, e:
            self.__exception = e

    def __coerce__(self, other):
        return (self.__val, other)
        
    def __getattr__(self, name):
        self.__thread.join()
        if self.__exception is not None:
            raise self.__exception
        out = getattr(self.__val, name)
        return out

def future(f):
    return Future(f)

@future
def long_running():
    print 'Starting long_running()'
    out = 0
    for i in range(LARGE):
        out += 1
    print 'Done with long_running()'
    return out

@future
def long_str():
    print 'Starting long_running()'
    out = 0
    for i in range(LARGE):
        out += 1
    print 'Done with long_running()'
    return str(out)

@future
def raises():
    raise Exception('This is a test')

print 'Getting value result from long running'
v = long_running()

print 'Doing other stuff ...'
print 'Use result of long_running()'
print v, LARGE
print v + v
print v
print xrange(v)

v = long_str()
print v[0]
print v * 2
print v.split

v = raises()
print v

# RESULT
'''
>>> import deferred
Getting value result from long running
Starting long_running()
Doing other stuff ...
Use result of long_running()
Done with long_running()
100000 100000
200000
100000
xrange(100000)
Starting long_running()
Done with long_running()
1
100000100000
<built-in method split of str object at 0x00B4E5C0>

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in -toplevel-
    import deferred
  File "C:\Python\Python24\deferred.py", line 72, in -toplevel-
    print v
  File "C:\Python\Python24\deferred.py", line 27, in __getattr__
    raise self.__exception
Exception: This is a test
>>> 
'''
