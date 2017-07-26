"""
The pyInterfaces module.

A simplified interface framework for Python.
"""


__version__ = '1.0'
__needs__ = '2.2'
__author__ = "G. Rodrigues"


class Interface(type):
    """The Interface metaclass."""

    def __init__(cls, name, bases, dct):
        super(Interface, cls).__init__(name, bases, dct)
        attribs = dct.keys()
        #Remove __metaclass__.
        attribs.remove('__metaclass__')
        #Store declared attributes => call super setattr.
        super(Interface, cls).__setattr__('__attributes__', attribs)

    #interfaces are "static" objects => we disallow dynamic changes.
    def __setattr__(cls, name, value):
        raise AttributeError("Cannot bind attributes in interface classes.")

    def __delattr__(cls, name):
        raise AttributeError("Cannot delete attributes in interface classes.")

    def attributes(cls):
        """Returns the list of noncallable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in cls.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if not callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def callables(cls):
        """Returns the list of callable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in cls.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def implements(cls, obj):
        """Returns 1 if obj implements interface cls, 0 otherwise."""
        #Check attributes.
        for attrib in cls.attributes():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError:
                return 0
            else:
                if callable(objattrib):
                    return 0
        #Check callables.
        for attrib in cls.callables():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError:
                return 0
            else:
                if not callable(objattrib):
                    return 0
        return 1


#Global function.
def implements(obj, *interfaces):
    """Returns 1 if obj implements *all* interfaces, 0 otherwise."""
    for interface in interfaces:
        if not interface.implements(obj):
            return 0
    return 1


#Test code and use cases.
if __name__ == '__main__':
    #Declaring an interface.
    class IStack(object):
        """The IStack interface."""

        __metaclass__ = Interface

        def __init__(self):
            """The initializer."""
            raise NotImplementedError

        def push(self, elem):
            """Push an element into the stack."""
            raise NotImplementedError

        def pop(self):
            """Pop an element from the stack."""
            raise NotImplementedError

    print IStack.__attributes__
    print IStack.attributes()
    print IStack.callables()

    #Are changes disallowed?
    try:
        IStack.__attributes__ = 1
    except AttributeError, x:
        print x

    #Declaring an IStack class.
    class Stack(object):
        """The Stack class implemented via nested tuples."""

        def __init__(self):
            """The initializer."""
            super(Stack, self).__init__()
            self.__head = None

        def push(self, elem):
            self.__head = (elem, self.__head)

        def pop(self):
            if self.__head is not None:
                ret, self.__head = self.__head
                return ret
            else:
                raise IndexError("Cannot get an element from an empty stack.")        

    #Instantiate Stack.
    s = Stack()

    if implements(s, IStack):
        print "Object %r behaves like an %r." % (s, IStack)
    else:
        print "Something is not right."

    #This shows why not checking signatures gives problems...
    if implements(Stack, IStack):
        print "Object %r behaves like an %r and it sucks :-(" % (Stack, IStack)
    else:
        print "Although right, something is not right."
