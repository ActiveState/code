import gc
import inspect

exclude = [
    "function",
    "type",
    "list",
    "dict",
    "tuple",
    "wrapper_descriptor",
    "module",
    "method_descriptor",
    "member_descriptor",
    "instancemethod",
    "builtin_function_or_method",
    "frame",
    "classmethod",
    "classmethod_descriptor",
    "_Environ",
    "MemoryError",
    "_Printer",
    "_Helper",
    "getset_descriptor",
    ]

def dumpObjects():
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if name not in exclude:
                filename = inspect.getabsfile(o.__class__)            
                print "Object of class:", name, "...",
                print "defined in file:", filename                

if __name__=="__main__":

    class TestClass:
        pass
        
    testObject1 = TestClass()
    testObject2 = TestClass()
    
    dumpObjects()
