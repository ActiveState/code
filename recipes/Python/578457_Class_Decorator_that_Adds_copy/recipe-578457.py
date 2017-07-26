import inspect


def get_init_params(cls):
    """Return the parameters expected when calling the class."""
    initializer = cls.__init__
    if initializer is object.__init__ and cls.__new__ is not object.__new__:
        initializer = cls.__new__
    try:
        return list(inspect.signature(initializer).parameters)[1:]
    except TypeError:
        return None


def copiable(fields=None):
    """A class decorator factory that adds a copy method to the class.

    If fields is not passed, the following a tried in order:

    1. cls.__all__
    2. cls._fields
    3. the parameters of cls.__init__
    4. the parameters of cls.__new__

    """
    if isinstance(fields, type):
        return copiable(None)(fields)

    if isinstance(fields, str):
        fields = fields.replace(',', ' ').split()

    def decorator(cls):
        """Return the class after adding the copy() method."""
        names = fields
        if names is None:
            names = getattr(cls, '__all__',
                            getattr(cls, '_fields',
                                    get_init_params(cls)))
        if names is None:
            raise TypeError("could not determine the fields for this class.")

        def copy(self, **kwargs):
            """Return a copy of this object, with updates."""
            ns = dict((name, getattr(self, name)) for name in names)
            ns.update(kwargs)
            return type(self)(**ns)

        method_name = '_copy' if 'copy' in names else 'copy'
        if hasattr(cls, method_name):
            raise TypeError("{!r} already exists on the class")
        setattr(cls, method_name, copy)
        return cls
    return decorator
