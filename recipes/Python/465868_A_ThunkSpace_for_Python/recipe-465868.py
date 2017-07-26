class ThunkSpace(object):
    """
    A ThunkSpace for Python. Assigning functions to an instance of ThunkSpace
    will turn the function into a lazily evaluated attribute.
    """
        
    def __setattr__(self, name, func):
        def delete(self):
            delattr(self.__class__, name)
        def get(self): 
            return func()
        def set(self, new_func):
            def get(self): 
                return new_func()
            setattr(self.__class__, name, property(get, set, delete))
        setattr(self.__class__, name, property(get, set, delete))
            
    
if __name__ == "__main__":    

    def lazy_something():
        return "lazy_something was called."
    
    def lazy_something_else():
        return "lazy_something_else was called."
    
    #create a ThunkSpace
    ts = ThunkSpace()
    
    #create an attribute named lazy_func, which when referenced, will call 
    #lazy_something
    ts.lazy_func = lazy_something
    
    print ts.lazy_func
    
    #the lazy_func attribute can be replaced with another function...
    ts.lazy_func = lazy_something_else
    
    print ts.lazy_func
    
