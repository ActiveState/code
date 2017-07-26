import sys as _sys

def subclass(bases, name, suite={}, doc=None):
    """Return a class that inherits from bases

    bases is the base class or classes, name is the name of the class, suite is a mapping of 
    attributes that the subclass should have.

    Unfortunately only the metaclass of the first base class will be used at class construction.  
    Suggestions on how to fix that are welcome. 
    """ 
    assert bases, "At least one base class must be supplied"
    if not hasattr(bases, '__iter__'):
        bases = (bases,)
    class cls(bases[0]):
        # We can't use the *bases form prior to Python 3.  If the later bases do anything clever in
        # thier metaclasses, we won't recieve their effects.  :-(
        locals().update(suite)
        # This seems to work reliably in CPython, it's not clear if that's standard
    cls.__name__ = name
    cls.__bases__ = bases
    # Stolen from the NamedTuple implementation
    if hasattr(_sys, '_getframe') and _sys.platform != 'cli':
        cls.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    if doc:
        cls.__doc__ = doc
    return cls
