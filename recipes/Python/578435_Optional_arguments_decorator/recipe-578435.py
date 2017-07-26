# callable is not in Python 3.0 and 3.1. We create our own if needed.
try:
    callable
except:
    import collections
    def callable(o):
        return isinstance(o, collections.Callable)

def isbuiltin(o):
    return isinstance(o, type) and o.__module__ in ["__builtin__", "builtins"]

_valid_target_defaults = {
    None: lambda o: not isinstance(o, type),
    "class": lambda o: isinstance(o, type) and not isbuiltin(o),
    "type": lambda o: isinstance(o, type),
    "any": lambda o: True,
    "never": lambda o: False
}

# opt_arg_dec_with_args (basically unique to the call):
#       (decorated_function, params, kwargs)
incompletely_used_decorators = {}

# In Python 3, i like to make the arguments keywork-only like this:
# def opt_arg_dec(decorated, *, is_method=False, valid_target=None):
def opt_arg_dec(decorated, is_method=False, valid_target=None, 
    allow_non_callable=False):
    """ 
    is_method: True if the function to become an opt_arg_dec is a 
        method or a classmethod (not a staticmethod).
    valid_target: A callable receiving a single object and returning True
        if it is a valid target for the decorator to decorate. 

        This is not used as error validation. This is to detect when the 
        decorator will only be called once (when no initial call to set 
        arguments is made or when it is not used in the form of a decorator.)
        If arguments were previously passed, the target will be sent through
        without any form of checking. You must still to error validation in
        your decorator if you need it.

        The target must be callable unless allow_non_callable is True.
        Special values:
        - None (default): the target must not be a type/class (but it can be
                an instance of a type/class).
                Use this for function decorator, unless you want to pass in
                a function to be more specific and only allow certain specific
                types.
        - "class": the target must be a class (not an instance of a class).
                However, builtin classes that are global to python will not
                be accepted. Meaning (int, float, str, set, dict, list, tuple
                and maybe a few more) since it is unlikely to want to decorate
                those.
                Use this for class decorators.
        - "type": same as "class", but builtin classes are also accepted.
        - "any": anything is allowed. (Must still be callable unless
                allow_non_callable is True)
        - "never": nothing will ever be accepted as target. This means the
                decorator must always be called before being applied to the
                real target, even if it means with no arguments.
    
    allow_non_callable: If False (the default), then the target to be
        decorated must be callable! See valid_target for more details,
        this check is done in the same conditions. Setting this to True means
        that valid_target must do more advanced check, otherwise almost
        anything will be considered a valid target and the first call to the
        function will be treated as a full call.
    """
    try:
        if valid_target in _valid_target_defaults:
            valid_target = _valid_target_defaults[valid_target]
    except:
        # valid_target is not hashable. So it's not one of the special values.
        pass

    is_method = bool(is_method)

    options = {"is_method": is_method,
               "valid_target": valid_target,
               "allow_non_callable": allow_non_callable}

    def opt_arg_dec_wrapped(*params, **kwargs):
        return _opt_arg_dec_used(decorated, options, params, kwargs)
    
    opt_arg_dec_wrapped.__name__ = decorated.__name__
    opt_arg_dec_wrapped.__doc__ = decorated.__doc__

    return opt_arg_dec_wrapped


# I don't want to nest all of that inside opt_arg_dec_wrapped! You are free to
# do so, but there is really little to be gained.

def _opt_arg_dec_used(decorated, options, params, kwargs):
    is_method = options["is_method"]

    # is_method is a bool. True == 1, False == 0
    if len(params) - is_method > 0:
        potential_target = params[is_method]

        if potential_target == Ellipsis:
            # We remove the Ellipsis from the parameters.
            params = params[0:is_method] + params[is_method+1:]

        elif ( (options["allow_non_callable"] or callable(potential_target)) 
            and options["valid_target"](potential_target) ):
            return decorated(*params, **kwargs)

        elif isinstance(potential_target, (classmethod, staticmethod)):
            raise TypeError(("Object of type %s passed in as first argument. " + 
                            "Might be expected or an error. If expected, " +
                            "pass Ellipsis as first argument, then the rest. " +
                            "Otherwise, fix the error. staticmethod and " +
                            "classmethod must be the higher decorator so that "+ 
                            "it is the last one called.")
                            % type(potential_target).__name__)

    def opt_arg_dec_with_args(target):
        incompletely_used_decorators.pop(opt_arg_dec_with_args, None)
        if is_method:
            return decorated(params[0], target, *params[1:], **kwargs)
        else:
            return decorated(target, *params, **kwargs)
            
    infos = (decorated, params, kwargs)
    incompletely_used_decorators[opt_arg_dec_with_args] = infos

    return opt_arg_dec_with_args

# The optional arguments decorator is itself an optional arguments decorator!
opt_arg_dec = opt_arg_dec(opt_arg_dec, valid_target="any")

def get_misused_opt_arg_dec():
    """ 
    Used to help developpers find places where an optionnal argument decorator
    was misused. 

    returns a list of (decorator, params, kwargs).

    Things appear in this list when a opt_arg_dec is called without a valid
    target and never called again. Example:

    @my_function_decorator
    class Foo(object):
        pass

    The decorator was expecting to receive a function, but received a class in
    the first call. If this was really what was desired, then you must call the
    decorator first to skip this validation:

    @my_function_decorator()
    class Foo(object):
        pass
    """
    return list(incompletely_used_decorators.values())
