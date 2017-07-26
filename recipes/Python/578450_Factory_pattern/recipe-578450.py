"""
A generic factory implementation.
Examples:
>>f=Factory()
>>class A:pass
>>f.register("createA",A)
>>f.createA()
<__main__.A instance at 01491E7C>

>>> class B:
... 	def __init__(self, a,b=1):
... 		self.a=a
... 		self.b=b
... 		
>>> f.register("createB",B,1,b=2)
>>> f.createB()
>>> b=f.createB()
>>> 
>>> b.a
1
>>> b.b
2

>>> class C:
... 	def __init__(self,a,b,c=1,d=2):
... 		self.values = (a,b,c,d)
... 
>>> f.register("createC",C,1,c=3)
>>> c=f.createC(2,d=4)
>>> c.values
(1, 2, 3, 4)

>>> f.register("importSerialization",__import__,"cPickle")
>>> pickle=f.importSerialization()
>>> pickle
<module 'cPickle' (built-in)>
>>> f.register("importSerialization",__import__,"marshal")
>>> pickle=f.importSerialization()
>>> pickle
<module 'marshal' (built-in)>

>>> f.unregister("importSerialization")
>>> f.importSerialization()
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
AttributeError: Factory instance has no attribute 'importSerialization'
"""

class Factory:      
    def register(self, methodName, constructor, *args, **kargs):
        """register a constructor"""
        _args = [constructor]
        _args.extend(args)
        setattr(self, methodName,apply(Functor,_args, kargs))
        
    def unregister(self, methodName):
        """unregister a constructor"""
        delattr(self, methodName)

class Functor:
    def __init__(self, function, *args, **kargs):
        assert callable(function), "function should be a callable obj"
        self._function = function
        self._args = args
        self._kargs = kargs
        
    def __call__(self, *args, **kargs):
        """call function"""
        _args = list(self._args)
        _args.extend(args)
        _kargs = self._kargs.copy()
        _kargs.update(kargs)
        return apply(self._function,_args,_kargs)
        
