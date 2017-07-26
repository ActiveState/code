import types

class Wrapper(object):
    def __init__(self,obj):
        self._obj = obj
    
    def __getattr__(self, attr):
        
        if hasattr(self._obj, attr):
            attr_value = getattr(self._obj,attr)
            
            if isinstance(attr_value,types.MethodType):
                def callable(*args, **kwargs):
                    return attr_value(*args, **kwargs)
                return callable
            else:
                return attr_value
            
        else:
            raise AttributeError
