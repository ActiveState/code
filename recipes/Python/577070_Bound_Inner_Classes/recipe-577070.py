"""
http://code.activestate.com/recipes/577070-bound-inner-classes/

Copyright (C) 2010-2011 by Alex Martelli and Larry Hastings

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__all__ = ["BoundInnerClass", "UnboundInnerClass"]

import weakref

class _Worker(object):
    def __init__(self, cls):
        self.cls = cls

    def __get__(self, outer, outer_class):
        if not outer:
            return self.cls

        name = self.cls.__name__

        # if we're already cached in outer, use that version
        # (but don't use getattr, that would call __get__ recursively)
        if name in outer.__dict__:
            return outer.__dict__[name]

        wrapper_bases = [self.cls]

        # iterate over cls's bases and look in outer to see
        # if any have bound inner classes in outer.
        # if so, multiply inherit from the bound inner version(s).
        multiply_inherit = False

        for base in self.cls.__bases__:
            # if we can't find a bound inner base,
            # add the original unbound base instead.
            # this is harmless but helps preserve the original MRO.
            inherit_from = base

            # if we inherit from a boundinnerclass from another outer class,
            # we might have the same name as a legitimate base class.
            # but if we look it up, we'll call __get__ recursively... forever.
            # if the name is the same as our own name, there's no way it's a
            # bound inner class we need to inherit from, so just skip it.
            if base.__name__ != name:
                bound_inner_base = getattr(outer, base.__name__, None)
                if bound_inner_base:
                    bases = getattr(bound_inner_base, "__bases__", (None,))
                    # the unbound class is always the first base of
                    # the bound inner class.
                    if bases[0] == base:
                        inherit_from = bound_inner_base
                        multiply_inherit = True
            wrapper_bases.append(inherit_from)

        Wrapper = self._wrap(outer, wrapper_bases[0])
        Wrapper.__name__ = name

        # Assigning to __bases__ is startling, but it's the only way to get
        # this code working simultaneously in both Python 2 and Python 3.
        if multiply_inherit:
            Wrapper.__bases__ = tuple(wrapper_bases)

        # cache in outer, but only if we're replacing the class
        # (if we're a bound inner class of A, and there's class B(A),
        #  and in class B we're some other kind of attribute,
        #  *don't* stomp on it!)
        if getattr(outer.__class__, name, None) == self.cls:
            setattr(outer, name, Wrapper)
        return Wrapper

class BoundInnerClass(_Worker):
    def _wrap(self, outer, base):
        wrapper_self = self
        assert outer
        outer_weakref = weakref.ref(outer)
        class Wrapper(base):
            def __init__(self, *args, **kwargs):
                wrapper_self.cls.__init__(self,
                                          outer_weakref(), *args, **kwargs)

            # give the bound inner class a nice repr
            # (but only if it doesn't already have a custom repr)
            if wrapper_self.cls.__repr__ is object.__repr__:
                def __repr__(self):
                    return "".join([
                        "<",
                        self.__module__,
                        ".",
                        self.__class__.__name__,
                        " object bound to ",
                        repr(outer_weakref()),
                        " at ",
                        hex(id(self)),
                        ">"])
        return Wrapper

class UnboundInnerClass(_Worker):
    def _wrap(self, outer, base):
        class Wrapper(base):
            pass
        return Wrapper


# The code in this "if" statement will only execute if you run the module
# directly; it won't run if you "import" this code into your own programs.
if __name__ == "__main__":
    class Outer(object):
        @BoundInnerClass
        class Inner(object):
            def __init__(self, outer):
                self.outer = outer

        @BoundInnerClass
        class SubclassOfInner(Inner.cls):
            def __init__(self, outer):
                super(Outer.SubclassOfInner, self).__init__()
                assert self.outer == outer

        @BoundInnerClass
        class SubsubclassOfInner(SubclassOfInner.cls):
            def __init__(self, outer):
                super(Outer.SubsubclassOfInner, self).__init__()
                assert self.outer == outer

        @BoundInnerClass
        class Subclass2OfInner(Inner.cls):
            def __init__(self, outer):
                super(Outer.Subclass2OfInner, self).__init__()
                assert self.outer == outer

        class RandomUnboundInner(object):
            def __init__(self):
                super(Outer.RandomUnboundInner, self).__init__()
                pass

        @BoundInnerClass
        class MultipleInheritanceTest(SubclassOfInner.cls,
                     RandomUnboundInner,
                     Subclass2OfInner.cls):
            def __init__(self, outer):
                super(Outer.MultipleInheritanceTest, self).__init__()
                assert self.outer == outer

        @UnboundInnerClass
        class UnboundSubclassOfInner(Inner.cls):
            pass


    def tests():
        assert outer.Inner == outer.Inner
        assert isinstance(inner, outer.Inner)
        assert isinstance(inner, Outer.Inner)

        assert isinstance(subclass, Outer.SubclassOfInner)
        assert isinstance(subclass, outer.SubclassOfInner)
        assert isinstance(subclass, Outer.Inner)
        assert isinstance(subclass, outer.Inner)

        assert isinstance(subsubclass, Outer.SubsubclassOfInner)
        assert isinstance(subsubclass, outer.SubsubclassOfInner)
        assert isinstance(subsubclass, Outer.SubclassOfInner)
        assert isinstance(subsubclass, outer.SubclassOfInner)
        assert isinstance(subsubclass, Outer.Inner)
        assert isinstance(subsubclass, outer.Inner)

    import itertools

    for order in itertools.permutations([1, 2, 3]):
        outer = Outer()
        # This strange "for" statement lets us test every possible order of
        # initialization for the "inner" / "subclass" / "subsubclass" objects.
        for which in order:
            if which == 1: inner = outer.Inner()
            elif which == 2: subclass = outer.SubclassOfInner()
            elif which == 3: subsubclass = outer.SubsubclassOfInner()
        tests()

    multiple_inheritance_test = outer.MultipleInheritanceTest()
    assert outer.MultipleInheritanceTest.mro() == [
        # bound inner class, notice lowercase-o "outer"
        outer.MultipleInheritanceTest,
        # unbound inner class, notice uppercase-o "Outer"
        Outer.MultipleInheritanceTest,
        outer.SubclassOfInner, # bound
        Outer.SubclassOfInner, # unbound
        Outer.RandomUnboundInner, # etc.
        outer.Subclass2OfInner,
        Outer.Subclass2OfInner,
        outer.Inner,
        Outer.Inner,
        object
    ]

    unbound = outer.UnboundSubclassOfInner()
    assert outer.UnboundSubclassOfInner.mro() == [
        outer.UnboundSubclassOfInner,
        Outer.UnboundSubclassOfInner,
        outer.Inner,
        Outer.Inner,
        object
    ]

    class InnerChild(outer.Inner):
        pass

    inner_child = InnerChild()

    isinstance(inner_child, Outer.Inner)
    isinstance(inner_child, InnerChild)
    isinstance(inner_child, outer.Inner)
