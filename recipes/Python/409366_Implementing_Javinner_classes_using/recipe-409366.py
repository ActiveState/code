def testInner():
    class Outer:
        def __init__(self,x): self.x = x

        # if python ever gets class decorators,
        # an inner class could be specified as:
        #@innerclass
        class Inner:
            def __init__(self, y): self.y = y
            def sum(self):  return self.x + self.y
        # as of python 2.4
        Inner = innerclass(Inner)

    outer = Outer('foo')
    inner = outer.Inner('bar'); assert inner.sum() == 'foobar'
    # outer.x, inner.x, inner.__outer__.x refer to the same object
    outer.x = 'moo'; assert inner.sum() == 'moobar'
    inner.x = 'zoo'; assert inner.sum() == 'zoobar'
    inner.__outer__.x = 'coo'; assert inner.sum() == 'coobar'
    # an inner class must be bounded to an outer class instance
    try: Outer.Inner('foo')
    except AttributeError, e: pass #print e
    else: assert False


def testStaticInner():
    class Outer:

        x = 'foo'

        class Nested:
            def __init__(self, y): self.y = y
            def sum(self): return self.x + self.y
        Nested = nestedclass(Nested)

    outer = Outer()
    nested = Outer.Nested('bar'); assert nested.sum() == 'foobar'
    nested.x = 'moo'; assert Outer.x == 'moo' and nested.sum() == 'moobar'
    nested.y = 'baz'; assert nested.sum() == 'moobaz'



def innerclass(cls):
    '''Class decorator for making a class behave as a Java (non-static) inner
    class.

    Each instance of the decorated class is associated with an instance of its
    enclosing class. The outer instance is referenced implicitly when an
    attribute lookup fails in the inner object's namespace. It can also be
    referenced explicitly through the property '__outer__' of the inner
    instance.
    '''
    if hasattr(cls, '__outer__'):
        raise TypeError('Cannot set attribute "__outer__" in inner class')
    class InnerDescriptor(object):
        def __get__(self,outer,outercls):
            if outer is None:
                raise AttributeError('An enclosing instance that contains '
                           '%s.%s is required' % (cls.__name__, cls.__name__))
            clsdict = cls.__dict__.copy()
            # explicit read-only reference to the outer instance
            clsdict['__outer__'] = property(lambda self: outer)
            # implicit lookup in the outer instance
            clsdict['__getattr__'] = lambda self,attr: getattr(outer,attr)
            def __setattr__(this, attr, value):
                # setting an attribute in the inner instance sets the
                # respective attribute in the outer instance if and only if
                # the attribute is already defined in the outer instance
                if hasattr(outer, attr): setattr(outer,attr,value)
                else: super(this.__class__,this).__setattr__(attr,value)
            clsdict['__setattr__'] = __setattr__
            return type(cls.__name__, cls.__bases__, clsdict)
    return InnerDescriptor()


def nestedclass(cls):
    '''Class decorator for making a class behave as a Java static inner class.

    Each instance of the decorated class is associated with its enclosing
    class. The outer class is referenced implicitly when an attribute lookup
    fails in the inner object's namespace. It can also be referenced
    explicitly through the attribute '__outer__' of the inner instance.
    '''
    if hasattr(cls, '__outer__'):
        raise TypeError('Cannot set attribute "__outer__" in nested class')
    class NestedDescriptor(object):
        def __get__(self, outer, outercls):
            clsdict = cls.__dict__.copy()
            # explicit read-only reference the outer class
            clsdict['__outer__'] = outercls
            # implicit lookup in the outer class
            clsdict['__getattr__'] = lambda self,attr: getattr(outercls,attr)
            def __setattr__(this, attr, value):
                # setting an attribute in the inner instance sets the
                # respective attribute in the outer class if and only if the
                # attribute is already defined in the outer class
                if hasattr(outercls, attr): setattr(outercls,attr,value)
                else: super(this.__class__,this).__setattr__(attr,value)
            clsdict['__setattr__'] = __setattr__
            return type(cls.__name__, cls.__bases__, clsdict)
    return NestedDescriptor()



if __name__ == '__main__':
    testInner()
    testStaticInner()
