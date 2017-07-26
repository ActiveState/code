#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import getmembers, ismethod

_NOVALUE = object()
class _Memoized(object):
    def __init__(self):
       self.value = _NOVALUE 

    def __nonzero__(self):
        return (self.value is not _NOVALUE)

class singleton(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        memoized = _Memoized()

        def singleton_wrapper(instance_self, *args, **kwargs):
            if args or kwargs:
                raise TypeError, ("Singleton-wrapped methods shouldn't take"
                        "any argument! (%s)" % self.func)                            
            if not memoized:
                memoized.value = self.func(instance_self)
            return memoized.value

        return singleton_wrapper

class prototype(object):
    def __init__(self, func):
        self.func = func

class _Container(object):
    def __call__(self, klass):
        subklass_dict = dict(klass.__dict__)
        self._set_singletons(subklass_dict, klass)
        self._set_prototypes(subklass_dict, klass)
        return type(klass.__name__, (klass, ), subklass_dict)

    def _set_singletons(self, subklass_dict, klass):
        for name, singletoned in ((n, f) for (n, f) in getmembers(klass, 
            lambda x: isinstance(x, singleton)) ):
            subklass_dict[name] = singletoned()

    def _set_prototypes(self, subklass_dict, klass):
        for name, prototyped in ((n, f) for (n, f) in getmembers(klass, 
            lambda x: isinstance(x, prototype))):
            subklass_dict[name] = prototyped.func

Container = _Container()

if __name__ == "__main__":

    class MySomething(object):
        pass

    class TheObject(object):
        def __init__(self, someattr):
            self.someattr = someattr

    class MyContainer(object):
        def __init__(self, config):
            self.config = config

        @singleton
        def theobject(self):
            return TheObject(self.config["someattr"])

        @prototype
        def something(self, value):
            o = MySomething()
            o.value = value
            o.obj = self.theobject()
            return o

    # python >= 2.6 users can use class decorators.
    MyContainer = Container(MyContainer)

    mc = MyContainer({"someattr": "a"})
    something1 = mc.something(1)
    something2 = mc.something(2)
    theobject = mc.theobject()
    
    assert theobject.someattr == "a"
    assert something1.value == 1
    assert something2.value == 2
    assert (something1.obj is something2.obj)
    assert (something2.obj is theobject) 
