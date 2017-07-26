"""
Rather than defining your get/set/del methods at the class level, as is usually done, e.g.

class MyClass(object):
    def __init__(self):
        self._foo = "foo"

    def getfoo(self):
        return self._foo
    def setfoo(self, value):
        self._foo = value
    def delfoo(self):
        del self._foo
    foo = property(getfoo, setfoo, delfoo, "property foo's doc string")

I would like to suggest the following alternative idiom:
"""


class MyClass(object):
    def __init__(self):
        self._foo = "foo"
        self._bar = "bar"

    def foo():
        doc = "property foo's doc string"
        def fget(self):
            return self._foo
        def fset(self, value):
            self._foo = value
        def fdel(self):
            del self._foo
        return locals()  # credit: David Niergarth
    foo = property(**foo())

    def bar():
        doc = "bar is readonly"
        def fget(self):
            return self._bar
        return locals()    
    bar = property(**bar())
