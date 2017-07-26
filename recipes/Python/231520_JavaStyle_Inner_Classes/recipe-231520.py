class Outer(object):
    class Inner(object):
        def __init__(self, outer):
            self.outer = outer

import new
Outer.Inner = new.instancemethod(Outer.Inner, None, Outer)

# That's it. Now you cannot create an Inner without an Outer.

# For a more self-contained solution using metaclasses:
def hasinnerclasses(classname, bases, d):
    import new, types
    klass = new.classobj(classname, bases, d)
    for name,cls in d.items():
        if isinstance(cls, (type, types.ClassType)):
            setattr(klass, name, new.instancemethod(cls, None, klass))
    return klass

class Outer(object):
    __metaclass__ = hasinnerclasses
    class Inner(object):
        def __init__(self, outer):
            self.outer = outer

    
>>> out = Outer()
>>> inr = out.Inner() # Note that *both* arguments are supplied automatically
>>> inr.outer is out
True

# Trying to cheat doesn't work...
>>> cheat = Outer.Inner() #fails
>>> cheat = Outer.Inner('foo') #also fails
