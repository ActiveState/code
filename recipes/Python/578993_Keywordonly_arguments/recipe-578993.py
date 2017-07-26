#!/usr/bin/python

from __future__ import print_function

import functools
import inspect


def decorator_factory(*kw_only_parameters):
    """Transforms a function with keyword arguments into one with
    keyword-only arguments.

    Call this decorator as @decorator_factory() for the default mode,
    which makes all keyword arguments keyword-only, or with the names
    of arguments to make keyword-only.  They must correspond with the
    names of arguments in the decorated function.  It works by
    collecting all the arguments into *args and **kws, then moving the
    arguments marked as keyword-only from **kws into *args.

    Args:
      *kw_only_parameters: Keyword-only arguments as strings.

    Returns:
      A decorator that modifies a function so it has keyword-only
      arguments.

    """
    def decorator(wrapped):
        """The decorator itself, assigns arguments as keyword-only and
        calculates sets for error checking.

        Args:
          wrapped: The function to decorate.

        Returns:
          A function wrapped so that it has keyword-only arguments.

        """

        # Each Python 3 argument has two independent properties: it is
        # positional-and-keyword *or* keyword-only, and it has a
        # default value or it doesn't.
        names, varargs, _, defaults = inspect.getargspec(wrapped)

        # If there are no default values getargpsec() returns None
        # rather than an empty iterable for some reason.
        if defaults is None:
            defaults = ()
        names_with_defaults = frozenset(names[len(names) - len(defaults):])
        names_to_defaults = dict(zip(reversed(names), reversed(defaults)))
        if kw_only_parameters:
            kw_only_names = frozenset(kw_only_parameters)
        else:
            kw_only_names = names_with_defaults.copy()

        @functools.wraps(wrapped)
        def wrapper(*args, **kws):
            """Wrapper function, checks arguments with set operations, moves args
            from **kws into *args, and then calls wrapped().

            Args:
              *args, **kws: The arguments passed to the original function.

            Returns:
              The original function's result when it's called with the
              modified arguments.

            Raises:
              TypeError: When there is a mismatch between the supplied
                and expected arguments.

            """

            new_args = []
            args_index = 0
            for name in names:
                if name in kws:
                    # Check first if there's a bound keyword for this name
                    new_args.append(kws.pop(name))
                elif name in kw_only_names:
                    # If this name is keyword-only, check for a
                    # default or raise.
                    if name in names_to_defaults:
                        new_args.append(names_to_defaults[name])
                    else:
                        _wrong_args(wrapped, names, 
                                    kw_only_names -
                                    (names_with_defaults | frozenset(kws)),
                                    'keyword-only')
                elif args_index < len(args):
                    # Check for a positional arg.
                    new_args.append(args[args_index])
                    args_index += 1
                elif name in names_to_defaults:
                    # Check for a default value.
                    new_args.append(names_to_defaults[name])
                else:
                    # No positional arg or default for this name so raise.
                    _wrong_args(wrapped, names,
                                frozenset(names) -
                                (names_with_defaults | frozenset(kws)),
                                'positional', len(args))

            if args_index != len(args) and not varargs:
                # Too many positional arguments and no varargs, so
                # raise after subtracting off the number of kw-only
                # arguments from those expected.
                raise TypeError(
                    '%s() takes %d positional arguments but %d were given' %
                    (wrapped.__name__,
                     len(names) - len(names_with_defaults | frozenset(kws)),
                     len(args)))
            else:
                # Pass the rest of the positional args, if any.
                new_args.extend(args[args_index:])

            return wrapped(*new_args, **kws)
        return wrapper

    return decorator


def _wrong_args(wrapped, names, missing_args, arg_type, number_of_args=0):
    """ Raise Python 3-style TypeErrors for missing arguments."""
    ordered_args = [a for a in names if a in missing_args]
    ordered_args = ordered_args[number_of_args:]
    error_message = ['%s() missing %d required %s argument' % 
                     (wrapped.__name__, len(ordered_args), arg_type)]
    if len(ordered_args) == 1:
        error_message.append(": '%s'" % ordered_args[0])
    else:
        error_message.extend(['s: ', 
                              ' '.join("'%s'" % a for a in ordered_args[:-1]),
                              " and '%s'" % ordered_args[-1]])
    raise TypeError(''.join(error_message))


if __name__ == '__main__':
    def test(f, *args, **kws):
        print(args, kws, '-> ', end='')
        try:
            f(*args, **kws)
        except TypeError as e:
            print(e.args[0])

    @decorator_factory()
    def f(a, b, c, d, e='e'):
        print(a, b, c, d, e)

    test(f)
    test(f, 0, 1, 2, 3)
    test(f, 0, 1, 2, 3, 4)

    @decorator_factory('c')
    def f(a, b, c='c', d='d', *args, **kws):
        print(a, b, c, d, args, kws)

    test(f)
    test(f, 0, 1)
    test(f, -1, b='b')
    test(f, b='b')
    test(f, 0)
    test(f, 0, 1, 2, 3, 4, 5, c='foo', d='bar', e='baz')

    @decorator_factory('b', 'c')
    def f(a, b, c='c', d='d', *args, **kws):
        print(a, b, c, d, args, kws)

    test(f, 0)
    test(f, 0, b='b')
    test(f, 0, 1, 2)
    test(f, 0, 1, 2, b='b')
    test(f, 0, 1, 2, 3, 4, 5, c='foo', d='bar', e='baz')
    test(f, 0, 1, 2, 3, 4, 5, b='foo', c='bar', e='baz')

    class C(object):
        @decorator_factory('b', 'c')
        def __init__(self, a, b, c='c', d='d', *args, **kws):
            print(a, b, c, d, args, kws)

    test(C, 0, 1, 2, b='b')
    test(C, 0, 1, 2, 3, 4, 5, b='foo', c='bar', e='baz')
