import inspect


def inheritdocstrings(cls):
    """A class decorator for inheriting method docstrings.

    >>> class A(object):
    ...   class_attr = True
    ...   def method(self):
    ...     '''Method docstring.'''

    >>> @inheritdocstrings
    ... class B(A):
    ...   def method(self):
    ...     pass

    >>> B.method.__doc__
    'Method docstring.'
    """
    for name, cls_attr in inspect.getmembers(cls, callable):
        if not name.startswith('_') and not cls_attr.__doc__:
            for c in cls.mro():
                if c is cls:
                    continue
                attr = c.__dict__.get(name)
                if attr and attr.__doc__:
                    try:
                        cls_attr.__func__.__doc__ = attr.__doc__
                    except (AttributeError, TypeError):
                        # Probably a read-only attribute, swallow it.
                        pass
                    break
    return cls
