from inspect import getargspec, formatargspec

_generator_with_attributes_redefinition = """
def decorated%(oldargs)s:
    wrapper = type('GeneratorWithAttributes', (object,),
                   {"__iter__":lambda self: wrapped})()
    wrapped = genfunc%(newargs)s
    for x in ("close", "next", "send", "throw", "gi_code", "gi_frame",
              "gi_running"):
        setattr(wrapper, x, getattr(wrapped, x))
    return wrapper
"""

def generator_with_attributes(genfunc):
    """Decorator to enable class-like attributes on a generator.

    `genfunc` should take `self` for its first parameter.

    Example:
    >>> def f(self, x):
    ...     while True:
    ...             print self
    ...             print dir(self)
    ...             yield x
    >>> dec = generator_with_attributes(f)
    >>> g = dec(1234)
    >>> g.next() # doctest: +ELLIPSIS
    <GeneratorWithAttributes object at 0x...>
    [...]
    1234
    >>> g.x = 123
    >>> g.next() # doctest: +ELLIPSIS
    <GeneratorWithAttributes object at 0x...>
    [...'x'...]
    1234

    """
    old = getargspec(genfunc)
    old[0].pop(0)
    new = getargspec(genfunc)
    new[0][0] = 'wrapper'
    specs = {'name': genfunc.func_name, 'oldargs': formatargspec(*old),
             'newargs': formatargspec(*new)}
    exec _generator_with_attributes_redefinition % specs in locals()
    decorated.__name__ = genfunc.__name__
    decorated.__doc__ = genfunc.__doc__
    return decorated

if __name__ == "__main__":
    import doctest
    doctest.testmod()
