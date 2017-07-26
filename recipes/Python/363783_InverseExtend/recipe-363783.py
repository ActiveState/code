"""Iterate downward through a hierarchy calling a method at each step."""

__docformat__ = "restructuredtext"


def inverseExtend(boundMethod, *args, **kargs):

    """Iterate downward through a hierarchy calling a method at each step.

    boundMethod -- This is the bound method of the object you're interested in.
    args, kargs -- The arguments and keyword arguments to pass to the
        top-level method.

    You can call this method via something like this:

        inverseExtend(object.method, myArg, myOtherArg)

    When calling the method at each step, I'll call it like this: 

        Class.method(object, callNext, *args, **kargs)

    However, the lowest level class's method has no callNext parameter,
    since it has no one else to call:

        Class.method(object, *args, **kargs)

    In the method:
    
        callNext(*args, **kargs) 
        
    should be called when it is time to transfer control to the subclass.  This
    may even be in the middle of the method.  Naturally, you don't have to pass
    *args, **kargs, but a common idiom is for the parent class to just receive
    *args and **kargs and pass them on unmodified.

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
            methods.insert(0, last)

    def callNext(*args, **kargs):
        """This closure is like super(), but it calls the subclass's method."""
        method = methods.pop()
        if len(methods):
            return method(obj, callNext, *args, **kargs)
        else:
            return method(obj, *args, **kargs)

    return callNext(*args, **kargs)


# Test out the code.
if __name__ == "__main__":

    from cStringIO import StringIO

    class A:
        def f(self, callNext, count):
            buf.write('<A count="%s">\n' % count)
            callNext(count + 1)
            buf.write('</A>')

    class B(A):
        # I don't have an f method, so you can skip me.
        pass

    class C(B):
        def f(self, callNext, count):
            buf.write('  <C count="%s">\n' % count)
            callNext(count + 1)
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
