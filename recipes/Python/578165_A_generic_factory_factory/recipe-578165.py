import contextlib

class Factory:
    """A generic instance factory that tracks the instances.

    A Factory must be created with the target type as its only
    non-keyword argument.

    """

    def __init__(self, *args, **defaults):
        self.type, = args
        self.defaults = defaults
        self.objects = set()

    def create(self, **kwargs):
        """Create and track a new instance of the factory's type."""
        fullkwargs = self.defaults.copy()
        fullkwargs.update(kwargs)
        obj = self.type(**fullkwargs)
        self.objects.add(obj)

    def remove(self, obj):
        """Remove the object."""
        # obj.__del__() should call obj.clear()
        self.objects.remove(obj)

    def clear(self):
        """Delete all the objects."""
        for obj in list(self.objects):
            self.remove(obj)

    @contextlib.contextmanager
    def one(self, **kwargs):
        """A context manager for temporary instances."""
        device = self.create(**kwargs)
        yield device
        self.clear(device)


factory = Factory(str, encoding='ascii', errors='replace')
name = factory.create(b"Lancelot")
