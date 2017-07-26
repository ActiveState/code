class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}
    
    def __init__(self,timeout=2):
        self.timeout = timeout
        
    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache
    
    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout
        
        def func(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                print "cache"
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                print "new"
                v = self.cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.func_name
        
        return func


#The code below demonstrates usage of the MWT decorator. Notice how the cache is
#cleared of some entries after the MWT().collect() method is called.

@MWT()
def z(a,b):
    return a + b

@MWT(timeout=5)
def x(a,b):
    return a + b

z(1,2)
x(1,3)

print MWT()._caches
#>>> {<function 'z'>: {(1, 2): (3, 1099276281.092)},<function 'x'> : {(1, 3): (4, 1099276281.092)}}

time.sleep(3)
MWT().collect()
print MWT()._caches
#>>> {<function 'z'>: {},<function 'x'> : {(1, 3): (4, 1099276281.092)}}
