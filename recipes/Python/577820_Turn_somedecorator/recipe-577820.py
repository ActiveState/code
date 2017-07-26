"""decorator module

"""

import functools


def has_default_decorator(decorator_factory):
    """A meta-decorator for decorator factories.

    This decorator of decorators allows a decorator factory to be used
    as a normal decorator (without calling syntax).

    A single non-keyword argument (with no keyword arguments) will be
    considered the object to be decorated.  If more than one argument
    is passed, or any keyword arguments are passed, all arguments will
    be passed to the decorator factory.

    To treat a single argument as an argument to the decorator factory,
    pass the keyword-only argument "lonely_argument=True".  It will
    default to False.

    """

    @functools.wraps(decorator_factory)
    def wrapper(*args, **kwargs):
        single_argument = kwargs.pop("lonely_argument", False)
        if not single_argument and len(args) == 1:
            return decorator_factory()(*args)
        return decorator_factory(*args, **kwargs)
    return wrapper
