"""kwonly module

"""

def emulate_kwonly(kws, required, withdefaults, leftovers=False):
    """Emulate Python 3's kwonly arguments.

    Parameters:
      kws - the kwargs from which to extract the kwonly args.
      required - an iterable holding the required kwonly args.
      withdefaults - an iterable of pairs mapping names to defaults.
      leftovers - allow kws to be non-empty when all the kwonly args
            have already been popped off.

    Returns:
      The remainder of kws, followed by the values for the kwonly args
      in the same order as they stand in required and then in
      withdefaults.

    Examples:
      Below each "def" clause you'll find the clause that would be
      equivalent in Python 3 to the use of emulate_kwonly().

      >>> def f(a, **kwargs):
      ... #def f(a, *, b, c=5):
      ...     kwargs, b, c = emulate_kwonly(kwargs, ("b",), (("c", 5),))
      ...     # continue as normal
      ...
      >>> def g(a, *args, **kwargs):
      ... #def f(a, *args, b, **kwargs):
      ...     kwargs, b = emulate_kwonly(kwargs, ("b",), (), True)
      ...     # continue as normal

    """

    if hasattr(withdefaults, "items"):
        # allows for OrderedDict to be passed
        withdefaults = withdefaults.items()

    kwonly = []

    # extract the required keyword-only arguments
    missing = []
    for name in required:
        if name not in kws:
            missing.append(name)
        else:
            kwonly.append(kws.pop(name))

    # validate required keyword-only arguments
    if len(missing) > 2:
        end = "s: %s, and %s" % (", ".join(missing[:-1]), missing[-1])
    elif len(missing) == 2:
        end = "s: %s and %s" % tuple(missing)
    elif len(missing) == 1:
        end = ": %s" % tuple(missing)
    if missing:
        msg = "missing %s required keyword-only argument%s"
        raise TypeError(msg % (len(missing), end))

    # handle the withdefaults
    for name, value in withdefaults:
        if name not in kws:
            kwonly.append(value)
        else:
            kwonly.append(kws.pop(name))

    # handle any leftovers
    if not leftovers and kws:
        msg = "got an unexpected keyword argument '%s'"
        raise TypeError(msg % (kws.keys()[0]))

    return [kws] + kwonly


if __name__ == "__main__":

    def f(a, **kwargs):
    #def f(a, *, b, c=5):
        kwargs, b, c = emulate_kwonly(kwargs, ("b",), (("c", 5),))
        return a, b, c

    assert f(1, b=2) == (1, 2, 5)
    assert f(1, b=2, c=3) == (1, 2, 3)

    try: f(b=2)
    except TypeError: pass
    else: raise AssertionError

    try: f(1, 2)
    except TypeError: pass
    else: raise AssertionError

    try: f(1, c=2)
    except TypeError: pass
    else: raise AssertionError

    try: f(1, b=2, d=4)
    except TypeError: pass
    else: raise AssertionError


    def g(a, *args, **kwargs):
    #def f(a, *args, b, **kwargs):
        kwargs, b = emulate_kwonly(kwargs, ("b",), (), True)
        return a, b, kwargs

    assert g(1, b=2) == (1, 2, {})
    assert g(1, b=2, c=3) == (1, 2, dict(c=3))
