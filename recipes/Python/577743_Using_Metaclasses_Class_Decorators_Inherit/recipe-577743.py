"""inherits_docstring module"""

def get_docstring(bases, name):
    for base in bases:
        if name not in base.__dict__:
            continue
        attr = getattr(base, name)
        if not hasattr(attr, "__doc__"):
            continue
        if attr.__doc__ is None:
            continue
        return attr.__doc__
    return None


def inherits_docstring_func(f, cls=None, funcname=None):
    """A function decorator for inheriting function docstrings.

    Look to cls for the docstring to inherit.  The funcname argument
    indicates that the cls should be searched for that name instead
    of f.__name__.

    """

    name = funcname
    if not name:
        name = f.__name__
    if cls is None:
        """shouldn't get here"""

    # go for it

    if funcname:
        docstring = get_docstring((cls,), name)
    else:
        docstring = None

    if docstring is None:
        docstring = get_docstring(cls.__bases__, name)
    if docstring is None and hasattr(cls, "__implements__"):
        # for registrations on ABCs
        docstring = get_docstring(cls.__implements__, name)

    if docstring is not None:
        f.__doc__ = docstring
    return f


def inherits_docstring(f, cls=None, funcname=None):
    """A decorator for inheriting function docstrings.

    If f is a class, return a decorator that looks to the class for
    the docstring to inherit.

    """
    if isinstance(f, type):
        #passed a class, so return a decorator
        cls = f
        def decorator(func):
            return inherits_docstring(func, cls)
        return decorator

    # otherwise used as decorator
    if cls is None:
        # don't know how to do this without a metaclass
        raise NotImplementedError
    return inherits_docstring_func(f, cls, funcname)


class DocDeco:
    """A class decorator tool for inheriting method docstrings.

    """

    class MethodWrapper:
        """decorator"""
        def __init__(self, f):
            self.f = f
    inherits_docstring = MethodWrapper

    def helps_docstrings(cls):
        """The class decorator."""

        for name, obj in cls.__dict__.items():
            if not isinstance(obj, DocDeco.MethodWrapper):
                # only act on decorated methods
                continue

            f = inherits_docstring(obj.f, cls)
            setattr(cls, name, f)

        return cls


class DocMeta(type):
    """A metaclass for inheriting method docstrings.

    """

    class MethodWrapper:
        """decorator"""
        def __init__(self, f):
            self.f = f
    inherits_docstring = MethodWrapper

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        for attr, obj in namespace.items():
            if not isinstance(obj, cls.MethodWrapper):
                # only act on decorated methods
                continue

            f = inherits_docstring(obj.f, cls)
            setattr(cls, attr, f)
