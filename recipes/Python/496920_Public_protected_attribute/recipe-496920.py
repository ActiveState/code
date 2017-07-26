def public(f):
    '''
    Decorator used to assign the attribute __public__ to methods.
    '''
    f.__public__ = True
    return f

class Protected(object):
    '''
    Base class of all classes that want to hide protected attributes from
    public access.
    '''
    def __new__(cls, *args, **kwd):
        obj = object.__new__(cls)        
        cls.__init__(obj, *args, **kwd)
                                
        def __getattr__(self, name):            
            attr = getattr(obj, name)
            if hasattr(attr, "__public__"):
                return attr
            elif hasattr(cls, "__public__"):
                if name in cls.__public__:
                    return attr                            
            raise AttributeError, "Attribute %s is not public."%name
        
        def __setattr__(self, name, value):
            attr = getattr(obj, name)                
            cls.__setattr__(self, name, value)    

        # Magic methods defined by cls must be copied to Proxy.
        # Delegation using __getattr__ is not possible.

        def is_own_magic(cls, name, without=[]):
            return name not in without and\
                   name.startswith("__") and name.endswith("__")

        Proxy = type("Protected(%s)"%cls.__name__,(),{})   

        for name in dir(cls):
            if is_own_magic(cls,name, without=dir(Proxy)):
                try:
                    setattr(Proxy, name, getattr(obj,name))
                except TypeError:
                    pass
                    
        
        Proxy.__getattr__ = __getattr__
        Proxy.__setattr__ = __setattr__
        return Proxy()

#
# Example
#

class Counter(Protected):
    __public__ = ["y"]
    def __init__(self, start=0):
        self.n = start
        self.y = 0
                    
    @public            
    def inc(self):
        self.n+=1
        return self.n
        
    @public        
    def dec(self):
        self.n-=1
        return self.n
    
    @public    
    def value(self):
        return self.n


#
# Enhanced example using inheritance
#

class SteppedCounter(Counter):
    def __init__(self, start=0, step=1):
        super(SteppedCounter,self).__init__(start=start)
        self.step = step

    @public            
    def inc(self):
        self.n+=self.step
        return self.n
    
    @public            
    def dec(self):
        self.n-=self.step
        return self.n
    
    def steps(self):
        return self.n/self.step


################################################################
#   Python Session
#################################################################

>>> c = Counter()
>>> c.inc()
1
>>> c.dec()
0
>>> c.n
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
  File "C:\Python24\Lib\site-packages\pythonwin\private.py", line 17, in __getattr__
    raise AttributeError, "Attribute %s is not public."%name
AttributeError: Attribute n is not public.
>>> c.y
0


>>> sc = SteppedCounter(step=2)
>>> sc.inc()
2
>>> sc.value()
2
>>> sc.steps()  
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
  File "C:\Python24\Lib\site-packages\pythonwin\private.py", line 17, in __getattr__
    raise AttributeError, "Attribute %s is not public."%name
AttributeError: Attribute steps is not public.
