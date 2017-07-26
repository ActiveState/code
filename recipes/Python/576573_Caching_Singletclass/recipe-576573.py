class CachedSingleton(object):
    """Provides caching singleton storage for data access decoration.
    Usage:
        class CachedSingletonClass(CachedSingleton):
            def _getitem(self, name):
                # implement data getting routine, such as db access
        
        CachedSingletonClass().attribute1 # returns value as if _getitem('attribute1') was called  
        CachedSingletonClass().attribute2 # returns value as if _getitem('attribute2') was called  
        CachedSingletonClass().__doc__ # returns real docstring  
    """    
    __instance = None
    
    def __new__(classtype, *args, **kwargs):
        if classtype != type(classtype.__instance):
            classtype.__instance = object.__new__(classtype, *args, **kwargs)
            classtype.__instance.cache = {}    
        
        return classtype.__instance
       
    # to be implemented by contract in the descendant classes
    def _getitem(self, name):
        return None
        
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            if not self.cache.has_key(name):
                self.cache[name] = self._getitem(name)
            return self.cache[name]
