class Singleton(type):
    """Creates a unique instance of classes that use Singleton as
    their metaclass.
    """

    def __new__(cls, name, bases, d):
        def __init__(self, *args, **kw):
            raise TypeError("cannot create '%s' instances" %
                            self.__class__.__name__)
        instance = type(name, bases, d)()
        instance.__class__.__init__ = __init__
        return instance
