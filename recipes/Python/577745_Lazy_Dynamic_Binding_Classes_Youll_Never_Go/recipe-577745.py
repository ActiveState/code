"""deferred_binder module"""

class DeferredBinder:
    """A descriptor that defers binding for an object.

    The binding is delayed until the name to which the descriptor is
    bound is accessed.  This is also the name to which the object would
    have been bound if the descriptor hadn't been used.

    """

    def __init__(self, name, target):
        self.name = name
        self.target = target

    def __get__(self, obj, cls):
        context = (cls.__dict__, cls)
        target = self.transform(self.name, context, self.target, obj)
        setattr(cls, self.name, self.target)
        return target

    @staticmethod
    def transform(name, context, target, obj=None):
        """Transform the target and return it.

          name - the name to which the target will be bound.
          context - namespace, and optionally the class, in which the
                target will be bound to the name.
          obj - the instance of the class that is involved in calling
                this method, if any.

        """
 
        return target

    @staticmethod
    def is_deferred(f):
        """A decorator."""
        return DeferredBinder(f.__name__, f)
