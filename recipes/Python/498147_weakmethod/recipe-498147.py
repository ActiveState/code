from weakref import proxy
from types import MethodType

class weakmethod(object):
    __slots__ = ["func"]
    def __init__(self, func):
        self.func = func
    def __get__(self, obj, cls):
        if obj is not None:
            obj = proxy(obj)
        return MethodType(self.func, obj, cls)

#######################################################

>>> class Foo(object):
...     @weakmethod
...     def bar(self, a, b):
...             print self, a, b
...
>>> f = Foo()
>>> b = f.bar
>>> b
<bound method Foo.bar of <weakproxy at 009FA1E0 to Foo at 009FC070>>
>>> b(1, 2)
<__main__.Foo object at 0x009FC070> 1 2

>>> del f
>>> b
<bound method Foo.bar of <weakproxy at 009FA1E0 to NoneType at 1E1D99B0>>
>>> b(1,2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in bar
ReferenceError: weakly-referenced object no longer exists
