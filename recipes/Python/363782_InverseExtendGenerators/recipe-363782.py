"""Iterate downward through a hierarchy calling a method at each step."""

__docformat__ = "restructuredtext"

import types


def inverseExtend(boundMethod, *args, **kargs):

    """Iterate downward through a hierarchy calling a method at each step.

    boundMethod -- This is the bound method of the object you're interested in.
    args, kargs -- The arguments and keyword arguments to pass to the
        top-level method.

    You can call this method via something like this:

        inverseExtend(object.method, myArg, myOtherArg)

    When calling the method at each step, I'll call it like this: 

        Class.method(object, *args, **kargs)

    Each parent class method *must* be a generator with exactly one yield
    statement (even if the yield statement never actually gets called), but the
    lowest level class method must *not* be a generator.  In the parent class:
    
        yield args, kargs

    should be called when it is time to transfer control to the subclass.  This
    may be in the middle of the method or not at all if the parent class does
    not wish for the child class's method to get a chance to run.  

    """

    # Build all the necessary data structures.

    obj = boundMethod.im_self
    methodName = boundMethod.im_func.__name__

    # Figure out the classes in the class hierarchy.  "classes" will
    # contain the most senior classes first.

    Class = obj.__class__
    classes = [Class]
    while Class.__bases__:
        Class = Class.__bases__[0]
        classes.insert(0, Class)

    # Skip classes that don't define the method.  Be careful with getattr
    # since it automatically looks in parent classes.  

    last = None
    methods = []
    for Class in classes:
        if (hasattr(Class, methodName) and 
            getattr(Class, methodName) != last):
            last = getattr(Class, methodName)
            methods.append(last)

    # Traverse down the class hierarchy.  Watch out for StopIteration's which
    # signify that the parent does not wish to call the child class's method.
    # generatorMethods maps generators to methods which we'll need for nice
    # error messages.

    generators = []
    generatorMethods = {}
    for method in methods[:-1]:
        generator = method(obj, *args, **kargs)
        assert isinstance(generator, types.GeneratorType), \
            "%s must be a generator" % `method`
        try:
            (args, kargs) = generator.next()
        except StopIteration:
            break
        generators.insert(0, generator)
        generatorMethods[generator] = method

    # If we didn't have to break, then the lowest level class's method gets to
    # run.

    else:
        method = methods[-1]
        ret = method(obj, *args, **kargs)
        assert not isinstance(ret, types.GeneratorType), \
            "%s must not be a generator" % method

    # Traverse back up the class hierarchy.  We should get StopIteration's at
    # every step.

    for generator in generators:
        try:
            generator.next()
            raise AssertionError("%s has more than one yield statement" %
                                 `generatorMethods[generator]`)
        except StopIteration:
            pass


# Test out the code.
if __name__ == "__main__":

    from cStringIO import StringIO

    class A:
        def f(self, count):
            buf.write('<A count="%s">\n' % count)
            yield (count + 1,), {}
            buf.write('</A>')

    class B(A):
        # I don't have an f method, so you can skip me.
        pass

    class C(B):
        def f(self, count):
            buf.write('  <C count="%s">\n' % count)
            yield (count + 1,), {}
            buf.write('  </C>\n')

    class D(C):
        def f(self, count):
            buf.write('    <D count="%s" />\n' % count)

    expected = """\
<A count="0">
  <C count="1">
    <D count="2" />
  </C>
</A>"""

    buf = StringIO()
    d = D()
    inverseExtend(d.f, 0)
    assert buf.getvalue() == expected
    buf.close()
