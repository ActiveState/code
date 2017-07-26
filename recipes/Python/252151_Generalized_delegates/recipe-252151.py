"""
This module creates Proxies that can also trap and delegate magic names.

Usage example:
>>> from proxy import *
>>> a = proxy([], ["__len__", "__iter__"])
>>> a
<proxy.listProxy object at 0x0113C370>
>>> a.__class__
<class 'proxy.listProxy'>
>>> a._obj
[]
>>> a.append
<built-in method append of list object at 0x010F1A10>
>>> a.__len__
<bound method listProxy.<lambda> of <proxy.listProxy object at 0x0113C370>>
>>> len(a)
0
>>> a.__getitem__
<method-wrapper object at 0x010F1AF0>
>>> a[1]
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
TypeError: unindexable object
>>> list(a)
[]
"""

class Proxy(object):
    """The Proxy base class."""

    def __init__(self, obj):
        """The initializer."""
        super(Proxy, self).__init__(obj)
        #Set attribute.
        self._obj = obj
        
    def __getattr__(self, attrib):
        return getattr(self._obj, attrib)


#Auxiliary getter function.
def getter(attrib):
    return lambda self, *args, **kwargs: getattr(self._obj, attrib)(*args, **kwargs)


def proxy(obj, names):
    """Factory function for Proxies that can delegate magic names."""
    #Build class.
    cls = type("%sProxy" % obj.__class__.__name__,
               (Proxy,),
               {})
    #Add magic names.
    for name in names:
        #Filter magic names.
        if name.startswith("__") and name.endswith("__"):
            if hasattr(obj.__class__, name):
                #Set attribute.
                setattr(cls, name, getter(name))
    #Return instance.
    return cls(obj)
