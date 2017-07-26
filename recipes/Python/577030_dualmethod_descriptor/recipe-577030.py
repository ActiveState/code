import functools

class dualmethod(object):
    """Descriptor implementing dualmethods (combination class/instance method).

    Returns a method which takes either an instance or a class as the first
    argument. When called on an instance, the instance is passed as the first
    argument. When called as a class, the class itself is passed instead.

    >>> class Example(object):
    ...     @dualmethod
    ...     def method(this):
    ...         if type(this) is type:
    ...             print "I am the class '%s'." % this.__name__
    ...         else:
    ...             print "I am an instance of the class '%s'." % this.__class__.__name__
    ...
    >>> Example.method()
    I am the class 'Example'.
    >>> Example().method()
    I am an instance of the class 'Example'.

    """
    def __init__(self, func):
        self.func = func
    def __get__(self, obj, cls=None):
        if cls is None:  cls = type(obj)
        if obj is None:  obj = cls
        @functools.wraps(self.func)
        def newfunc(*args, **kwargs):
            return self.func(obj, *args, **kwargs)
        return newfunc
