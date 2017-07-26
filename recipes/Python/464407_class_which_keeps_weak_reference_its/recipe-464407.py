import weakref

class InstanceTracker(object):
    def __new__(typ, *args, **kw):
        #check the class has an __instances__ dict, if not, 
        #create it and initialize __instance_id.
        try:
            typ.__instances__
        except AttributeError:
            typ.__instance_id = 0
            typ.__instances__ = weakref.WeakValueDictionary()
        obj = object.__new__(typ, *args, **kw)
        obj.id = typ.__instance_id
        typ.__instances__[typ.__instance_id] = obj
        typ.__instance_id += 1
        return obj
        
if __name__ == "__main__":        
    class AClass(InstanceTracker): pass
    class BClass(InstanceTracker): pass
    
    instances = [(AClass(),BClass()) for i in xrange(5)]
    
    for id, instance in AClass.__instances__.items():
        print id, instance, instance.id
    
    for id, instance in BClass.__instances__.items():
        print id, instance, instance.id
