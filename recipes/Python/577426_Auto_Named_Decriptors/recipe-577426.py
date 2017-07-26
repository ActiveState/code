class NamedDescriptor(object):
    def __init__(self):
        # Name of the attribute, will be set by the classes with
        # the meta class DescriptorNameGetterMetaClass
        self.name = None

    def __get__(self, obj, type=None):
        if obj:
            # at the moment, we return the name of the descriptor, 
            # you can change this line to adapt to your needs
            return self.name
        else:
            return self

    def __set__(self, adaptor, value):
        if adaptor:
            # change the name, you can change this line to adapt to your needs
            self.name = value
        else:
            raise AttributeError('Cannot set this value')


class NamedDescriptorResolverMetaClass(type):
    '''
    This is where the magic happens.
    '''
    def __new__(cls, classname, bases, classDict):
        # Iterate through the new class' __dict__ and update all recognised NamedDescriptor member names
        for name, attr in classDict.iteritems():
            if isinstance(attr, NamedDescriptor):
                attr.name = name
        return type.__new__(cls, classname, bases, classDict)

    
class DescriptorHost(object):
    '''
    The Descriptor gets its name automatically even before any instance of the class is created,
    thanks MetaClass!
    >>> DescriptorHost.myFunDescriptor.name
    'myFunDescriptor'

    In our case, the NamedDescriptor returns it's name when being looked for from the host instance:
    >>> dh = DescriptorHost()
    >>> dh.myFunDescriptor
    'myFunDescriptor'
    '''
    __metaclass__ = NamedDescriptorResolverMetaClass

    myFunDescriptor = NamedDescriptor()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
