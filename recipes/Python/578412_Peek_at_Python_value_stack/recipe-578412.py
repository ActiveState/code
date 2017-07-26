"""
valuestack.py: Demo reading values from Python value stack
Offsets are derived for CPython-2.7.2, 64-bit, production build

air:~ dima$ python valuestack.py 
return 0.0911498238164
caught 0.0911498238164
"""
import ctypes, inspect, random

def id2obj(i):
    """convert CPython `id` back to object ref, by temporary pointer swap"""
    tmp = None,
    try:
        ctypes.cast(id(tmp), ctypes.POINTER(ctypes.c_ulong))[3] = i
        return tmp[0]
    finally:
        ctypes.cast(id(tmp), ctypes.POINTER(ctypes.c_ulong))[3] = id(None)

def introspect():
    """pointer on top of value stack is id of the object about to be returned
    FIXME adjust for sum(vars, locals) in the introspected function
    """
    fr = inspect.stack()[1][0]
    print "caught", id2obj(ctypes.cast(id(fr), ctypes.POINTER(ctypes.c_ulong))[47])

def value():
    tmp = random.random()
    print "return", tmp
    return tmp

def foo():
    try:
        return value()
    finally:
        introspect()

if __name__ == "__main__":
    foo()
