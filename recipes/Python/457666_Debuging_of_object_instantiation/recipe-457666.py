import inspect
import gc

class Debug(object):

    " Subclass for collection of debugging informations "

    def __new__(cls, *a, **b):
        # Get the frame where the instantiation came from
        frame = inspect.stack()[1]
        # Continue with __new__ in super objects
        o = super(Debug, cls).__new__(cls, a, b)
        # Save important frame infos in object
        o.debug_call = list(frame[1:4]) + [frame[4][0]]
        return o

    def DebugInfo(self):
        # Split our informations
        file, line, module, source = self.debug_call
        # Format informative output
        return 'Object instantiated in file "%s", line %s, in %s: %s' % (
            file, 
            line, 
            module, 
            source.strip() )

def DumpDebugObjects(title):
    print "***", title, "***"
    gc.collect()
    for o in gc.get_objects():
        if isinstance(o, Debug):
            print o.DebugInfo()
            
if __name__=="__main__":
  
    class Test(Debug):
    
        def __init__(self, arg):
            print "Test", arg    
    
    class Test2(Test):
    
        pass
                                
    t1 = Test(1)
    t2 = Test(2)
    t3 = Test(3)

    DumpDebugObjects("We expect 3 objects")

    del t2
    
    DumpDebugObjects("Now one less")
    
