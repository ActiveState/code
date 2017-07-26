import types

def cachedmethod(function):
    return types.MethodType(Memoize(function), None)


class Memoize:
    def __init__(self,function):
        self._cache = {}
        self._callable = function
            
    def __call__(self, *args, **kwds):
        cache = self._cache
        key = self._getKey(*args,**kwds)
        try: return cache[key]
        except KeyError:
            cachedValue = cache[key] = self._callable(*args,**kwds)
            return cachedValue
    
    def _getKey(self,*args,**kwds):
        return kwds and (args, ImmutableDict(kwds)) or args    


class ImmutableDict(dict):
    '''A hashable dict.'''

    def __init__(self,*args,**kwds):
        dict.__init__(self,*args,**kwds)
    def __setitem__(self,key,value):
        raise NotImplementedError, "dict is immutable"
    def __delitem__(self,key):
        raise NotImplementedError, "dict is immutable"
    def clear(self):
        raise NotImplementedError, "dict is immutable"
    def setdefault(self,k,default=None):
        raise NotImplementedError, "dict is immutable"
    def popitem(self):
        raise NotImplementedError, "dict is immutable"
    def update(self,other):
        raise NotImplementedError, "dict is immutable"
    def __hash__(self):
        return hash(tuple(self.iteritems()))


if __name__ == '__main__':
    from math import sqrt,log,sin,cos
        
    class Example:
        def __init__(self,x,y):
            # self._x and self._y should not be changed after initialization
            self._x = x
            self._y = y
        
        @cachedmethod
        def computeSomething(self, alpha, beta):
            w = log(alpha) * sqrt(self._x * alpha + self._y * beta)
            z = log(beta) * sqrt(self._x * beta + self._y * alpha)
            return sin(z) / cos(w)
