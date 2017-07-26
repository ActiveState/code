"""deferred_default_arg module

Deferred is singleton to be used in place of None as the sentinel
for deferred default arguments.

"""

import inspect

class DeferredType: pass
Deferred = DeferredType()


def handle_deferred(f, name, fname=None):
    """Turn the singleton Deferred object into a default arg.

      f - the function to which you will pass the argument.
      name - the local name that will be passed as the argument.
      fname - the argument name of f.  If this is not passed, the name
            is used.

    If the argument of f() doesn't have a default value, raise a
    TypeError.  This is what would normally happen if you tried to call
    f() without passing that argument.  That's effectively what you are
    doing in that situation when passing Deferred.

    This function is a lot simpler if you use the PEP 362 function
    signature object.

    """

    if not fname:
        fname = name
    val = inspect.stack()[1][0].f_locals[name]
    if val is not Deferred:
        return val

    notkwonlycount = f.__code__.co_argcount - f.__code__.co_kwonlyargcount
    if fname in f.__code__.co_varnames[notkwonlycount:]:
        try:
            return f.__kwdefaults__[fname]
        except KeyError:
            raise TypeError("Can't convert Deferred for {}".format(name))
    default_names = f.__code__.co_varnames[
            notkwonlycount - len(f.__defaults__):notkwonlycount]
    try:
        return f.__defaults__[default_names.index(fname)]
    except ValueError:
        raise TypeError("Can't convert Deferred for {}".format(name))
