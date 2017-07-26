import sys

class _super (object):
    """
    Wrapper for the super object.

    If called, a base class method of the same name as the current method
    will be called. Otherwise, attributes will be accessed.
    """

    __name__ = 'super'

    # We want the lowest overhead possible - both speed and memory
    # We need to put the mangled name in as Python 2.2.x didn't work
    # with private names specified in __slots__.
    __slots__ = ('_super__super', '_super__method')

    def __init__(self, super, name):
        object.__setattr__(self, '_super__super', super)

        try:
            object.__setattr__(self, '_super__method', getattr(super, name))
        except AttributeError:
            object.__setattr__(self, '_super__method', name)

    def __call__(self, *p, **kw):
        """
        Calls the base class method with the passed parameters.
        """

        # We want fastest performance in the normal case - i.e. calling
        # self.super(*p, **kw). We don't care as much about how long it
        # takes to fail.
        method = object.__getattribute__(self, '_super__method')

        try:
            return method(*p, **kw)
        except TypeError:
            if type(method) is not str:
                raise

        # This should throw an AttributeError, but they could have modified
        # the base class
        super = object.__getattribute__(self, '_super__super')
        method = getattr(super, method)
        object.__setattr__(self, '_super__method', method)
        return method(*p, **kw)

    def __getattribute__ (self, name):
        """
        Gets a base class attribute.
        """

        super = object.__getattribute__(self, '_super__super')

        try:
            return getattr(super, name)
        except (TypeError, AttributeError):
            # Cannot call like self.super.super - produces inconsistent results.
            if name == 'super':
                raise TypeError("Cannot get 'super' object of 'super' object")

            raise

    def __setattr__(self, name, value):
        """
        All we want to do here is make it look the same as if we called
        setattr() on a real `super` object.
        """
        super = object.__getattribute__(self, '_super__super')
        object.__setattr__(super, name, value)

def _getSuper (self):
    """
    Gets the `super` object for the class of the currently-executing method.
    """
    frame = sys._getframe().f_back
    code = frame.f_code
    name = code.co_name

    # Find the method we're currently running by scanning the MRO and comparing
    # the code objects. When we find a match, that *might* be the class we're
    # currently in - however, we need to keep searching until we fail to find
    # a match. This is due to the way that methods are created - if you have
    #
    # class A (autosuper):
    #     def test (self):
    #         pass
    #
    # class B (A):
    #     pass
    #
    # then calling getattr(B, 'test') will return A.test, with no way to
    # determine that it's A.test. We only want to use this after calling 
    # getattr(A, 'test') otherwise we will determine the wrong class.

    cur_class = None

    for c in type(self).__mro__:
        try:
            m = getattr(c, name)
            func_code = m.func_code
        except AttributeError:
            func_code = None

        if func_code is code:
            cur_class = c
        elif cur_class is not None:
            break

    if cur_class is None:
        # We could fail to find the class if we're called from a function
        # nested in a method
        raise TypeError, "Can only call 'super' in a bound method"

    return _super(super(cur_class, self), name)

class autosuper (object):
    """
    Automatically determine the correct super object and use it.
    """

    # We want the lowest overhead possible - both speed and memory
    __slots__ = ()

    super = property(fget=_getSuper,
                     doc=_getSuper.__doc__.strip())
