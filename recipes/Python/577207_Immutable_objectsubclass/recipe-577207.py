class Immutable(object):
     """An immutable class.
     """
     _mutable = False
     def __setattr__(self, name,value):
        if self._mutable or name == '_mutable':
             super(Immutable,self).__setattr__(name,value)
        else:
             raise TypeError("Can't modify immutable instance")
    
     def __delattr__(self,name):
         if self._mutable:
             super(Immutable,self).__delattr__(name)
         else:
             raise TypeError("Can't modify immutable instance")
    
    
def mutablemethod(f):
    def func(self,*args, **kwargs):
        if isinstance(self,Immutable):
            old_mutable = self._mutable
            self._mutable = True
            res = f(self,*args, **kwargs)
            self._mutable = old_mutable
        else:
            res = f(self,*args, **kwargs)
        return res
    return func
         


if __name__ == '__main__':
    
    class A(Immutable):
        '''
           Define __init__ can set attributes for instance
        '''
        @mutablemethod
        def __init__(self,value):
            super(A,self).__init__(self)
            self.value = value
    
        def try_change(self,value):
            self.value = value
        
    a = A("test")
    a.try_change("TEST")
    a.value = "TEST"
