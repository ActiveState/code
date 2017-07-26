#!/usr/bin/env python
"""
>>> class A(Finalized):
...     __finalattrs__ = 'count',
...     items = []
...     def __init__(self):
...         super(A, self).__init__()
...         self.count = 0
...     def increment(self):
...         self.count += 1
...     def clear(self):
...         self.count = 0
...     def __finalize__(self):
...         super(A, self).__finalize__()
...         # access to final attributes
...         print 'Finalizing:', self.count
...         # access to methods
...         self.clear()
...         # access to class attributes
...         self.items.append(self.count)
... 
>>> a = A()
>>> a.increment()
>>> a.increment()
>>> a.count
2
>>> A.items
[]
>>> del a
Finalizing: 2
>>> A.items
[0]
>>> # inheritance works as normal
>>> class B(A):
...     __finalattrs__ = 'foo', 'bar'
...     def __init__(self, foo, bar):
...         super(B, self).__init__()
...         self.foo = foo
...         self.bar = bar
...     def __finalize__(self):
...         super(B, self).__finalize__()
...         print 'Removing:', self.foo, self.bar
...         
>>> b = B(42, 'badger')
>>> b.increment()
>>> del b
Finalizing: 1
Removing: 42 badger
"""

import weakref as _weakref


class _FinalizeMetaclass(type):
    # list of weak references; when the objects they reference
    # disappear, their callbacks will remove them from this set
    _reflist = set()
    
    def __init__(cls, name, bases, class_dict):
        super(_FinalizeMetaclass, cls).__init__(name, bases, class_dict)

        # add a descriptor for each final attribute that
        # delegates to the __base__ object
        for attr_name in class_dict.get('__finalattrs__', []):
            setattr(cls, attr_name, _FinalAttributeProxy(attr_name))

    def __call__(cls, *args, **kwargs):
        # create a new instance, set __base__, then initialize
        obj = cls.__new__(cls, *args, **kwargs)
        base = object.__new__(cls)
        obj.__base__ = base.__base__ = base
        obj.__init__(*args, **kwargs)

        # a closure for calling the class's __finalize__ method,
        # passing it just the instance's base object
        def get_finalize_caller(cls, base):
            def finalize_caller(ref):
                _FinalizeMetaclass._reflist.remove(ref)
                cls.__finalize__(base)
            return finalize_caller

        # register a weak reference to call the __finalize__        
        finalize_caller = get_finalize_caller(obj.__class__, obj.__base__)
        _FinalizeMetaclass._reflist.add(_weakref.ref(obj, finalize_caller))

        # return the newly created instance
        return obj


class _FinalAttributeProxy(object):
    """Redirects all {get,set,del}attr calls to the __base__ object"""
    def __init__(self, name):
        self.base_name = '_base_' + name
    def __get__(self, obj, objtype):
        return getattr(obj.__base__, self.base_name)
    def __set__(self, obj, value):
        setattr(obj.__base__, self.base_name, value)
    def __delete__(self, obj):
        delattr(obj.__base__, self.base_name)
    

class Finalized(object):
    __metaclass__ = _FinalizeMetaclass

    __finalattrs__ = ()    

    def __finalize__(self):
        """Release any resources held by the object.

        Only methods, class attributes, and the list of instance
        attributes named in the class's __finalattrs__ will be
        available from this method.
        """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
