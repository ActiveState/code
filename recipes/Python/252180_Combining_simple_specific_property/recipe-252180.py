import sys

def attribute(attrname, permit='rwd', fget=None, fset=None, fdel=None, doc=''):
    """returns a property associated with 'attrname'.
    
       By default, a simple property with get, set, and delete methods
       will be created. Optionally, specific get/set/del methods may be
       supplied. You can also choose to omit the creation of one or more
       of the default get/set/del methods via the 'permit' flag:
           'r': readable, 'w':writable, 'd':deletable
       So, if you want a property that is readable and deletable, but not
       writable, use "permit='rd'".
    """
    if _isprivate(attrname):
        attrname = _mangle(_get_classname(), attrname)
    if 'r' in permit and fget is None:
        fget = lambda self: getattr(self, attrname)
    if 'w' in permit and fset is None:
        fset = lambda self, value: setattr(self, attrname, value)
    if 'd' in permit and fdel is None:
        fdel = lambda self: delattr(self, attrname)
    return property(fget, fset, fdel, doc)

def _isprivate(attrname):
    return attrname.startswith("__") and not attrname.endswith("__")

def _mangle(classname, attrname):
    '''mangles name according to python name-mangling 
       conventions for private variables'''
    return "_%s%s" % (classname, attrname)

def _get_classname():
    "returns the calling class' name"
    frame = sys._getframe(2)
    classname = frame.f_code.co_name
    return classname

# example
if __name__ == "__main__":
    class C(object):
        a = attribute('_a', fget=lambda self: self._a*2)
        def __init__(self):
            self._a = "A"

    c = C()
    print c.a  # uses a.fget, user supplied
    c.a = "AA" # uses a.fset, provided by default
    print c.a
