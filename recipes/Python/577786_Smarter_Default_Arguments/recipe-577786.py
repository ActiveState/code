"""smart_default_arguments module

DEFERRED is the singleton to use in place of None as the sentinel
for deferred default arguments.

"""

import inspect


# mutable default arguments

def recalculate_defaults(f, newdefaults):
    argspec = inspect.getfullargspec(f)

    # take care of defaults

    args = argspec.args
    defaults = list(argspec.defaults)
    num_bare_args = len(args) - len(defaults)

    for i in range(len(args)-num_bare_args):
        defaults[i] = newdefaults.pop(args[i+num_bare_args], defaults[i])

    bare_args = args[:num_bare_args]
    while bare_args:
        arg = bare_args.pop()
        if arg in newdefaults:
            defaults = [newdefaults.pop(arg)] + defaults
        else:
            break

    # take care of kwonly defaults

    kwonly = argspec.kwonlyargs[:]
    kwdefaults = argspec.kwonlydefaults
    num_bare_kwonly = len(kwonly) - len(kwdefaults or ())

    for arg in kwonly[num_bare_kwonly:]:
        kwdefaults[arg] = newdefaults.pop(arg, kwdefaults[arg])
    
    bare_kwonly = kwonly[:num_bare_kwonly]
    while bare_kwonly:
        arg = bare_kwonly.pop()
        if arg in newdefaults:
            kwdefaults[arg] = newdefaults.pop(arg)
        else:
            break

    # finish up
    if newdefaults:
        raise TypeError("Unexpected new defaults: %s" % newdefaults)
    return tuple(defaults), kwdefaults


def has_default_arguments(**kwargs):
    """A decorator factory that applies default arguments.

    It handles mutable default arguments, which sets it apart from the
    normal handling of default arguments.

    Trust that kwargs matches parameters of the decorated function.

    """

    def decorator(f):
        f.__defaults__, f.__kwdefaults__ = recalculate_defaults(f, kwargs)
        return f
    return decorator


# deferred default arguments

import functools


class DEFER_DEFAULT_TYPE:
    """Indicates that the default argument should be deferred to the callee."""
DEFERRED = DEFER_DEFAULT_TYPE()


ERROR_MSG = "A DEFERRED object cannot be used for a non-default argument"

def recalculate_arguments(args, kwargs, 
                          spec_args, num_spec_args, num_bare_args, defaults,
                          kwonlyargs, kwonlydefaults):
    args = list(args)
    num_args = len(args)

    # handle argspec.args
    for i in range(num_spec_args):
        arg = spec_args[i]
        if i >= num_bare_args:
            if i < num_args and args[i] is DEFERRED:
                args[i] = defaults[i-num_bare_args]
            elif kwargs.get(arg) is DEFERRED:
                kwargs[arg] = defaults[i-num_bare_args]
            continue
        if i < num_args and args[i] is DEFERRED:
            raise TypeError(ERROR_MSG)
        elif kwargs.get(arg) is DEFERRED:
            raise TypeError(ERROR_MSG)

    # handle argspec.kwonlyargs
    defaults = kwonlydefaults
    for arg in kwonlyargs:
        if kwargs[arg] != DEFERRED:
            continue
        if arg not in kwonlydefaults:
            raise TypeError(ERROR_MSG)
        kwargs[arg] = kwonlydefaults[arg]

    return args, kwargs


def accepts_deferred_defaults(f):
    """A decorator that handles DEFERRED arguments.

    Because this wraps the decorated function with another function,
    performance will take a hit.  However, this is unavoidable since the
    arguments are not known until runtime.  Some effort has been made to
    optimize the new function, though it could certainly be improved.
    
    """

    argspec = inspect.getfullargspec(f)
    spec_args = argspec.args
    num_spec_args = len(spec_args)
    defaults = argspec.defaults
    num_bare_args = num_spec_args - len(defaults)
    kwonlyargs = argspec.kwonlyargs
    kwonlydefaults = argspec.kwonlydefaults

    @functools.wraps(f)
    def newfunc(*args, **kwargs):
        args, kwargs = recalculate_arguments(args, kwargs,
                           spec_args, num_spec_args, num_bare_args, defaults,
                           kwonlyargs, kwonlydefaults)
        return f(*args, **kwargs)
    return newfunc
