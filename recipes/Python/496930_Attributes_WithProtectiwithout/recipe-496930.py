class WithProtection(object):
    '''
    WithProtection can be used as a base class for all classes that 
    want true protection of user defined attributes mangled with a 
    single underscore "_". 
    '''    
    def __new__(cls, *args, **kwd):        
        obj = object.__new__(cls)        
        cls.__init__(obj, *args, **kwd)
        
        def __getattr__(self, name):            
            attr = getattr(obj, name)
            if name.startswith("_"):
                if name.startswith("__") and name.endswith("__"):
                    return attr
            else:
                return attr
            raise AttributeError, "Attribute %s is not public."%name
        
        def __setattr__(self, name, value):
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError,"magic attributes are write protected."
            attr = getattr(obj, name)                    
            cls.__setattr__(self, name, value)
                    
        # Magic methods defined by cls must be copied to Proxy.
        # Delegation using __getattr__ is not possible.

        def is_own_magic(cls, name, without=[]):
            return name not in without and\
                   name.startswith("__") and name.endswith("__")

        Proxy = type("WithProtection(%s)"%cls.__name__,(),{})
        
        for name in dir(cls):
            if is_own_magic(cls,name, without=dir(Proxy)):
                try:
                    setattr(Proxy, name, getattr(obj,name))
                except TypeError:
                    pass
                
        Proxy.__getattr__ = __getattr__        
        Proxy.__setattr__ = __setattr__
        proxy = Proxy()        
        return proxy 

#
# Example
#

class Counter(WithProtection):    
    def __init__(self, start=0):
        self._n = start
                    
    def inc(self):
        self._n+=1
        return self._n
            
    def dec(self):
        self._n-=1
        return self._n    
    
    def value(self):
        return self._n

#
# Enhanced example using inheritance
#

class SteppedCounter(Counter):
    def __init__(self, start=0, step=1):
        super(SteppedCounter,self).__init__(start=start)
        self.step = step        
    
    def inc(self):
        self._n+=self.step
        return self._n
    
    def __add__(self, k):
        return self._n+k
    
    def dec(self):
        self._n-=self.step
        return self._n
    
    def steps(self):
        return self._n/self.step

################################################################
#   Python Session
################################################################

>>> sc = SteppedCounter()
>>> sc.step
1
>>> sc._n
Traceback (most recent call last):
  ....
AttributeError: Attribute _n is not public.
>>> sc.inc()
1
>>> sc+8
9
