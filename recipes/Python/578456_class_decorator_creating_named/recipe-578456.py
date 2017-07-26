from collections import namedtuple as namedtuple


def as_namedtuple(*fields_and_global_default, **defaults):
    """A class decorator factory joining the class with a namedtuple.

    If any of the expected arguments are not passed to the class, they
    are set to the specific default value or global default value (if any).

    """
    num_args = len(fields_and_global_default)
    if num_args > 2 or num_args < 1:
        raise TypeError("as_namedtuple() takes at 1 or 2 positional-only "
                        "arguments, {} given".format(num_args))
    else:
        fields, *global_default_arg = fields_and_global_default
        if isinstance(fields, str):
            fields = fields.replace(',', ' ').split()

    for field in defaults:
        if field not in fields:
            raise ValueError("got default for a non-existant field ({!r})"
                             .format(field))

    # XXX unnecessary if namedtuple() got support for defaults.
    @classmethod
    def with_defaults(cls, *args, **kwargs):
        """Return an instance with defaults populated as necessary."""
        # XXX or dynamically build this method with appropriate signature
        for field, arg in zip(fields, args):
            if field in kwargs:
                raise TypeError("with_defaults() got multiple values for "
                                "keyword argument {!r}".format(field))
            kwargs[field] = arg
        for field, default in defaults.items():
            if field not in kwargs:
                kwargs[field] = default
        if global_default_arg:
            default = global_default_arg[0]
            for field in fields:
                if field not in kwargs:
                    kwargs[field] = default
        return cls(**kwargs)

    def decorator(cls):
        """Return a new nametuple-based subclass of cls."""
        # Using super() (i.e. the MRO) makes this work correctly.
        bases = (namedtuple(cls.__name__, fields), cls)
        namespace = {'__doc__': cls.__doc__, '__slots__': (),
                     'with_defaults': with_defaults}
        return type(cls.__name__, bases, namespace)
    return decorator
