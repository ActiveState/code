"""This class is a curry (think functional programming)."""

__docformat__ = "restructuredtext"


class Curry:

    """This class is a curry (think functional programming).

    The following attributes are used:

    f
      This is the function being curried.

    initArgs, initKargs
      These are the args and kargs to pass to ``f``.

    """

    def __init__(self, f, *initArgs, **initKargs):
        """Accept the initial arguments and the function."""
        self.f = f
        self.initArgs = initArgs
        self.initKargs = initKargs

    def __call__(self, *args, **kargs):
        """Call the function."""
        updatedArgs = self.initArgs + args
        updatedKargs = self.initKargs.copy()
        updatedKargs.update(kargs) 
        return self.f(*updatedArgs, **updatedKargs)
