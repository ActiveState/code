"""

An alternate implementation of bound inner classes.
    http://code.activestate.com/recipes/577623-bound-inner-classes-using-an-alternate-approach/

See also, the original approach:
    http://code.activestate.com/recipes/577070-bound-inner-classes/

Copyright (C) 2011 by Larry Hastings

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

__all__ = ["BindingOuterClass", "BoundInnerClass", "UnboundInnerClass"]

import weakref


class BindingOuterClass(object):
    def __getattribute__(self, name):
        attr = super(BindingOuterClass, self).__getattribute__(name)
        bind_request = getattr(attr, '_binding_class', False)
        suitable = isinstance(attr, type) and bind_request
        if not suitable:
            return attr

        wrapper_bases = [attr]

        # iterate over attr's bases and look in self to see
        # if any have bound inner classes in self.
        # if so, multiply inherit from the bound inner version(s).
        multiply_inherit = False

        for base in attr.__bases__:
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
                bound_inner_base = getattr(self, base.__name__, None)
                if bound_inner_base:
                    bases = getattr(bound_inner_base, "__bases__", (None,))
                    # the unbound class is always the first base of
                    # the bound inner class.
                    if bases[0] == base:
                        inherit_from = bound_inner_base
                        multiply_inherit = True
            wrapper_bases.append(inherit_from)

        Wrapper = attr._binding_class(attr, self, wrapper_bases[0])
        Wrapper.__name__ = name

        # Assigning to __bases__ is startling, but it's the only way to get
        # this code working simultaneously in both Python 2 and Python 3.
        if multiply_inherit:
            Wrapper.__bases__ = tuple(wrapper_bases)

        # cache in self
        setattr(self, name, Wrapper)

        return Wrapper


class BoundInnerClass(object):
    @staticmethod
    def _binding_class(attr, outer, base):
        assert outer
        outer_weakref = weakref.ref(outer)
        class Wrapper(base):
            # occlude the original _binding_class!
            # otherwise we'll recurse forever.
            _binding_class = None
            def __init__(self, *args, **kwargs):
                attr.__init__(self, outer_weakref(), *args, **kwargs)

            # give the bound inner class a nice repr
            # (but only if it doesn't already have a custom repr)
            if attr.__repr__ is object.__repr__:
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


class UnboundInnerClass(object):
    @staticmethod
    def _binding_class(attr, outer, base):
        class Wrapper(base):
            # occlude the original _binding_class!
            # otherwise we'll recurse forever.
            _binding_class = None

        return Wrapper


# The code in this "if" statement will only execute if you run the module
# directly; it won't run if you "import" this code into your own programs.
if __name__ == "__main__":
    class Outer(BindingOuterClass):
        class Inner(BoundInnerClass):
            def __init__(self, outer):
                self.outer = outer

        class SubclassOfInner(Inner):
            def __init__(self, outer):
                super(Outer.SubclassOfInner, self).__init__()
                assert self.outer == outer

        class SubsubclassOfInner(SubclassOfInner):
            def __init__(self, outer):
                super(Outer.SubsubclassOfInner, self).__init__()
                assert self.outer == outer

        class Subclass2OfInner(Inner):
            def __init__(self, outer):
                super(Outer.Subclass2OfInner, self).__init__()
                assert self.outer == outer

        class RandomUnboundInner(object):
            def __init__(self):
                super(Outer.RandomUnboundInner, self).__init__()
                pass

        class MultipleInheritanceTest(SubclassOfInner,
                     RandomUnboundInner,
                     Subclass2OfInner):
            def __init__(self, outer):
                super(Outer.MultipleInheritanceTest, self).__init__()
                assert self.outer == outer

        class UnboundSubclassOfInner(UnboundInnerClass, Inner):
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
        BoundInnerClass,
        object
        ]

    unbound = outer.UnboundSubclassOfInner()
    assert outer.UnboundSubclassOfInner.mro() == [
        outer.UnboundSubclassOfInner,
        Outer.UnboundSubclassOfInner,
        UnboundInnerClass,
        outer.Inner,
        Outer.Inner,
        BoundInnerClass,
        object
        ]

    class InnerChild(outer.Inner):
        pass

    inner_child = InnerChild()

    isinstance(inner_child, Outer.Inner)
    isinstance(inner_child, InnerChild)
    isinstance(inner_child, outer.Inner)
