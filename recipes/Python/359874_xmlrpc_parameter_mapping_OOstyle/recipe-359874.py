import re, time, xmlrpclib
from SimpleXMLRPCServer import *
import threading

class SomeState(object):
    def __init__(self):
        self.value = 0
        
    
CLASSES = [SomeState]
TIMEOUT = 60.0 * 5.0

class Timeout:
    pass
    
class InvalidId:
    pass
    
class ObjectManager(object):
    """ ObjectManager stores and  manages id-to-object mappings. It utilizes the 
    Borg pattern to avoid global variables.
    """
    shared_state = {"id2o" : {}}
    
    def __init__(self):
        self.__dict__ = self.shared_state
        
    def map(self, val, classes):
        """ Checks if a val is of a type found in classes and 
        then creates the mapping between the id of the value and
        a tuple constisting of the value itself and the current time.
        """
        if val.__class__ in classes:
            vid = id(val)
            self.id2o[vid] = (val, time.time())
            val = vid
        return val

    def lookup(self, vid, timeout):
        """ Lookups the passed vid in the o2id-mapping. If not found,
        a InvalidId exception is raised. If found, but the timeout kicks in, a 
        Timeout exception is raised. Otherwise the associated value is returned.
        """
        try:
            o, ts = self.id2o[vid]
            now = time.time()
            if now - ts > timeout:
                raise Timeout()
            self.id2o[vid] = (o, now)
            return o
        except KeyError:
            raise InvalidId()

            
def map(classes=CLASSES):
    """
    Registers a result value in the ObjectManager. The optional classes argument specifies
    the list of instances that are subject to mapping.
    """
    def f(func):
        def _map(self, *args, **kwargs):
            om = ObjectManager()
            res = func(self, *args, **kwargs)
            return om.map(res, classes)
        return _map
    return f
    
def lookup(poslist=[0], timeout=TIMEOUT):
    """
    Lookups the values at the indices listed in poslist in the ObjectManager.
    """    
    def f(func):
        def _lookup(self, *args, **kwargs):
            args = list(args)        
            om = ObjectManager()
            for pos in poslist:
                args[pos] = om.lookup(args[pos], timeout=timeout)
            return func(self, *args, **kwargs)
        return _lookup
    return f
    

def wrap(poslist=[0], timeout=TIMEOUT, classes=CLASSES):
    """
    Cobines lookup and map.
    """    
    def f(func):
        def _wrap(self, *args, **kwargs):
            args = list(args)        
            om = ObjectManager()
            for pos in poslist:
                args[pos] = om.lookup(args[pos], timeout=timeout)
            res = func(self, *args, **kwargs)
            return om.map(res, classes)
        return _wrap
    return f

    

class Test(object):
    
    @map()
    def init(self):
        return SomeState()
        
    @lookup()
    def add(self, state, amount):
        state.value += amount
        return state.value
    
    @wrap(timeout=1.0)
    def clone(self, state):
        ns = SomeState()
        ns.value = state.value
        return ns

    @lookup(poslist=[0,1])
    def equals(self, a, b):
        print a.value , b.value
        return a.value == b.value
        
    
def launch():
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(Test())
    server.serve_forever()

    
def main():
    server_thread = threading.Thread(target=launch)
    server_thread.setDaemon(True)   
    server_thread.start()
    # We need some time to start the server - this should be enough.
    time.sleep(4)
    t = xmlrpclib.ServerProxy("http://localhost:8000")
    
    # test mapping
    h = t.init()
    # test lookup
    h_value = t.add(h, 10)
    # test wrap
    cloned_h = t.clone(h)
    assert cloned_h != h
    cloned_h_value = t.add(cloned_h, 10)
    assert cloned_h_value == 20 and h_value == 10
    # test the timeout
    time.sleep(2)
    try:
        cloned_h = t.clone(h)
        assert False
    except xmlrpclib.Fault:
        pass
    # test the poslist 
    assert not t.equals(h, cloned_h)
    
if __name__ == "__main__":
    main()
    
