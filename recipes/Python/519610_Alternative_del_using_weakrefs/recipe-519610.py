#!/usr/bin/env python
"""
>>> class Demo(safedel):
...     __coreattrs__ = ['count']
...     bird = 'European'
...     def __init__(self):
...         super(Demo, self).__init__()
...         self.count = 5
...     @coremethod
...     def __safedel__(core):
...         super(Demo.__coreclass__, core).__safedel__()
...         print "Count:", core.count
...     @coremethod
...     def bridgekeeper(core):
...         # core instances can also access class attributes of the
...         # original class
...         return "%s swallow" % core.bird

>>> d = Demo()

# The core can still access attributes of the main class
>>> print d.bridgekeeper()
European swallow
>>> Demo.bird = 'African'
>>> print d.bridgekeeper()
African swallow

# Any attribute listed in __coreattr__ goes to the core object instead
>>> print d.count
5
>>> d.count = 3
>>> del d
Count: 3
"""

import weakref

__all__ = ['safedel', 'coremethod']


try:
    reflist = set()  # python2.4.  More efficient
except:
    class FakeSet(dict):
        def add(self, item):
            self[item] = None
        def remove(self, item):
            del self[item]
    reflist = FakeSet()  # Python2.2 or Python2.3


class SafedelMetaclass(type):
    def __init__(cls, name, bases, newattrs):
        #super(SafedelMetaclass, cls).__init__(name, bases, newattrs)
        type.__init__(name, bases, newattrs)

        attrs = {}
        for base in bases:
            for attrname in getattr(base, '__coreattrs__', []):
                attrs[attrname] = None
        for attrname in newattrs.get('__coreattrs__', []):
            attrs[attrname] = None

        def coregetattr(core, name):
            return getattr(core.__surfaceclass__, name)

        corebases = []
        for base in bases:
            x = getattr(base, '__coreclass__', None)
            if x is not None:
                corebases.append(x)
        corebases = tuple(corebases)

        newcoreattrs = {}
        newcoreattrs['__surfaceclass__'] = cls
        newcoreattrs['__getattr__'] = coregetattr

        for key, value in newattrs.items():
            if isinstance(value, coremethod):
                # coremethods need to know what name they have, but they
                # don't trust the info available when created, so we
                # supply it here instead.
                value.name = key
                newcoreattrs[key] = value.func

        coreclass = type(name + '__Core', corebases, newcoreattrs)

        cls.__coreclass__ = coreclass
        for attrname in attrs:
            setattr(cls, attrname, CoreAttrProxy(attrname))


class CoreAttrProxy(object):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype):
        if obj is None:  # Called from the class, somehow...
            raise AttributeError, 'Attribute %s not found' % self.name
        return object.__getattribute__(obj.__core__, self.name)

    def __set__(self, obj, value):
        object.__setattr__(obj.__core__, self.name, value)

    def __delete__(self, obj):
        # Slots erroneously don't raise AttributeError if the attribute
        # doesn't exist, so we use getattr to raise AttributeError anyway.
        getattr(obj.__core__, self.name)
        object.__delattr__(obj.__core__, self.name)


class coremethod(object):
    __slots__ = ['func', 'name']
    # name is set by SafedelMetaclass

    def __init__(self, func):
        try:
            if func.im_self is None:
                func = func.im_func  # Skip through unbound methods
        except AttributeError:
            pass  # Not a method at all
        self.func = func

    def __get__(self, obj, objtype):
        if obj is None:
            return self.func
        else:
            def boundcoremethod(*args, **kwargs):
                return getattr(obj.__core__, self.name)(*args, **kwargs)
            return boundcoremethod


class safedel(object):
    __metaclass__ = SafedelMetaclass
    def __init__(self, *args, **kwargs):
        super(safedel, self).__init__(*args, **kwargs)
        self.__core__ = self.__coreclass__()

        def outer(core, cls):
            def inner(ref):
                reflist.remove(ref)
                try:
                    cls.__safedel__(core)
                except:
                    import traceback
                    traceback.print_exc()
            return inner
        reflist.add(weakref.ref(self, outer(self.__core__, self.__class__)))

    def __safedel__(core):
        f = getattr(super(safedel.__coreclass__, core), '__safedel__', None)
        if f:
            f.__safedel__()
    __safedel__ = coremethod(__safedel__)


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
