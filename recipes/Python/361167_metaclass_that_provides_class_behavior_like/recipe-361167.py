import new
import inspect

class RubyMetaClass(type):
    """
    """
    def __new__(self, classname, classbases, classdict):
        try:
            frame = inspect.currentframe()
            frame = frame.f_back
            if frame.f_locals.has_key(classname):
                old_class = frame.f_locals.get(classname)
                for name,func in classdict.items():
                    if inspect.isfunction(func):
                        setattr(old_class, name, func)
                return old_class
            return type.__new__(self, classname, classbases, classdict)
        finally:
            del frame

class RubyObject(object):
    """
    >>> class C:
    ...   def foo(self): return "C.foo"
    ...
    >>> c = C()
    >>> print c.foo()
    C.foo
    >>> class C(RubyObject):
    ...   def bar(self): return "C.bar"
    ...
    >>> print c.bar()
    C.bar
    """
    __metaclass__ = RubyMetaClass
