def immutable(mutableclass):
    """ Decorator for making a slot-based class immutable """

    if not isinstance(type(mutableclass), type):
        raise TypeError('@immutable: must be applied to a new-style class')
    if not hasattr(mutableclass, '__slots__'):
        raise TypeError('@immutable: class must have __slots__')

    class immutableclass(mutableclass):
        __slots__ = ()                      # No __dict__, please   

        def __new__(cls, *args, **kw):
            new = mutableclass(*args, **kw) # __init__ gets called while still mutable
            new.__class__ = immutableclass  # locked for writing now
            return new 

        def __init__(self, *args, **kw):    # Prevent re-init after __new__
            pass

    # Copy class identity:
    immutableclass.__name__ = mutableclass.__name__
    immutableclass.__module__ = mutableclass.__module__

    # Make read-only:
    for name, member in mutableclass.__dict__.items():
        if hasattr(member, '__set__'):
            setattr(immutableclass, name, property(member.__get__))

    return immutableclass
