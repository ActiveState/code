import time
import threading

class Cache:
    "A cached function"

#   a dict of sets, one for each instance of this class
    __allInstances = set() # where the cached values are actually kept

    maxAge = 3600 # the default max allowed age of a cache entry (in seconds)
    collectionInterval = 2 # how long to wait between collection events
    __stopCollecting = False

    def __init__(self, func):
        Cache.__allInstances.add(self)
        self._store = {}
        self.__func = func

    def __del__(self):
        if self in Cache.__allInstances:
            Cache.__allInstances.remove(self)

    def __call__(self, *args, **kw):
        key = (args, tuple(sorted(kw.items())))
        if self._store.has_key(key):
            return self._store[key][1]

        result = self.__func(*args, **kw)
        self._store[key] = (time.time(), result)
        return result

    def invalidate(self):
        "Invalidate all cache entries for this function"
        self._store.clear()

    def invalidate_one(self, *args, **kw):
        "Invalidate the cache entry for a particular set of arguments for this function"
        key = (args, tuple(sorted(kw.items())))
        if self._store.has_key(key):
            del self._store[key]

    def collect(self):
        "Clean out any cache entries in this store that are currently older than allowed"
        now = time.time()
        for key, v in self._store.items():
            t, value = v # creation time, function output
            if self.maxAge > 0 and now - t > self.maxAge: # max ages of zero mean don't collect
                del self._store[key]

    @classmethod
    def collectAll(cls):
        "Clean out all old cache entries in all functions being cached"
        for instance in cls.__allInstances:
            instance.collect()

    @classmethod
    def _startCollection(cls):
        "Periodically clean up old entries until the stop flag is set"

        while cls.__stopCollecting is not True:
            time.sleep(cls.collectionInterval)
            cls.collectAll()

    @classmethod
    def startCollection(cls):
        "Start the automatic collection process in its own thread"

        cls.collectorThread = threading.Thread(target=cls._startCollection)
        cls.collectorThread.setDaemon(False)
        cls.collectorThread.start()

    @classmethod
    def stopCollection(cls):
        cls.__stopCollecting = True

# -------------------
# Example usage:

@Cache
def foo(arg):
    print 'foo called with arg=%s' % arg
    return arg*2

@Cache
def bar(arg1, arg2=3):
    print 'bar called with arg1=%s arg2=%s' % (arg1, arg2)
    return arg1 + arg2

foo(2) # cache misses, foo invoked, cache entry created for arg=2
foo(2) # cache hit, cached value retrieved
foo.invalidate() # all cache entries for foo are deleted (in this case, only 1)
foo(2) # cache misses, etc.

bar(1) # cache misses, cache entry created for arg1=1, arg2=3
bar(1, 3) # cache hit
bar(1, 2) # cache misses, cache entry created for arg1=1, arg2=2
bar.invalidate_one(1, 3)
bar(1, 3) # cache miss
bar(1, 2) # cache hit

Cache.collectionInterval = 1.5
Cache.startCollection() # starts cache collection for all funcs every 1.5 seconds
foo(2) # cache hit
foo.maxAge = 1 # set the max age for foo's (and only foo's) cache entries to 1 second
# wait a second
foo(2) # cache miss
Cache.stopCollection()
# ------------------
