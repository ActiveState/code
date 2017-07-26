import weakref
 
 
class weakattr(object):
    """
    weakattr - a weakly-referenced attribute. When the attribute is no longer
    referenced, it 'disappears' from the instance. Great for cyclic references.
    """
    __slots__ = ["dict", "errmsg"]
    
    def __init__(self, name = None):
        self.dict = weakref.WeakValueDictionary()
        if name:
            self.errmsg = "%%r has no attribute named %r" % (name,)
        else:
            self.errmsg = "%r has no such attribute"
    
    def __repr__(self):
        return "<weakattr at 0x%08X>" % (id(self),)
    
    def __get__(self, obj, cls):
        if obj is None:
            return self
        try:
            return self.dict[id(obj)]
        except KeyError:
            raise AttributeError(self.errmsg % (obj,))
    
    def __set__(self, obj, value):
        self.dict[id(obj)] = value
    
    def __delete__(self, obj):
        try:
            del self.dict[id(obj)]
        except KeyError:
            raise AttributeError(self.errmsg % (obj,))

#
# example
#
>>> class x(object):
...     next = weakattr()
...     def __init__(self):
...         self.next = self
...     def __del__(self):
...         print "g'bye"
...
>>>
>>> y = x()
>>> y.next
<__main__.x object at 0x009EFA50>
>>> del y
>>> gc.collect()
g'bye
0
