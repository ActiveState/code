import inspect
 
def mixin(cls):
    """
    mixes-in a class (or a module) into another class. must be called from within
    a class definition. `cls` is the class/module to mix-in
    """
    locals = inspect.stack()[1][0].f_locals
    if "__module__" not in locals:
        raise TypeError("mixin() must be called from within a class definition")
    
    # copy the class's dict aside and perform some tweaking
    dict = cls.__dict__.copy()
    dict.pop("__doc__", None)
    dict.pop("__module__", None)
    
    # __slots__ hell
    slots = dict.pop("__slots__", [])
    if slots and "__slots__" not in locals:
        locals["__slots__"] = ["__dict__"]
    for name in slots:
        if name.startswith("__") and not name.endswith("__"):
            name = "_%s%s" % (cls.__name__, name)
        dict.pop(name)
        locals["__slots__"].append(name)
    
    # mix the namesapces
    locals.update(dict)

#
# example
#
>>> class SomeMixin(object):
...     def f(self, x):
...         return self.y + x
...
>>> class AnotherMixin(object):
...     def g(self):
...         print "g"
...
>>>
>>> class Foo(object):
...     mixin(SomeMixin)
...     mixin(AnotherMixin)
...     
...     def h(self):
...         print "h"
...
