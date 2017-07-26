from __future__ import nested_scopes
import new


def enhance__init__(klass, f):
    ki = klass.__init__
    klass.__init__ = new.instancemethod(
        lambda *args, **kwds: f(ki, *args, **kwds),None,klass)


def demo():
    class X:
        def __init__(self,v):
            self.v = v

    def g(__init__, self, v):
        __init__(self, v)
        self.parrot='dead'

    enhance__init__(X, g)

    x = X(2)
    print x.parrot

demo()
