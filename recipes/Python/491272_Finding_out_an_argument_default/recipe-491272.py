def get_arg_default(func, arg_name):
    import inspect
    args, varargs, varkwargs, defaults = inspect.getargspec(func)
    have_defaults = args[-len(defaults):]

    if arg_name not in args:
        raise ValueError("Function does not accept arg '%s'" % arg_name)

    if arg_name not in have_defaults:
        raise ValueError("Parameter '%s' doesn't have a default value" % arg_name)

    return defaults[list(have_defaults).index(arg_name)]
