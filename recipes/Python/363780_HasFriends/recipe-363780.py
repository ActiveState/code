"""This mixin supports autoloading of "friend" methods."""

__docformat__ = "restructuredtext"

from Curry import Curry


class HasFriends:

    """This mixin supports autoloading of "friend" methods.

    That means if you have a class like ``aquarium.widget.FormUtil``, and you
    try to call a function ``fooBar`` on that class, ``FormUtil`` (assuming it
    mixes in this class) will automatically import
    ``aquarium.widget.formutil.fooBar`` (notice that the ``FormUtil`` class is
    automatically associated with the ``formutil`` package) and return the
    ``fooBar`` function.  ``fooBar`` will behave as if it were actually a
    method inside ``FormUtil``.  ``fooBar`` should be implemented as a normal
    method that just happens to receive a ``FormUtil`` instance named ``self``
    as its first argument.

    """

    def __getattr__(self, attr):
        """Return the desired friend method.
        
        Note, these methods will be cached in ``self._friendCache``.

        """
        if not self.__dict__.has_key("_friendCache"):
            self._friendCache = {}
        cache = self._friendCache 
        if not cache.has_key(attr):
            pieces = self.__module__.split(".")
            pieces[-1] = pieces[-1].lower()
            pieces.append(attr)
            moduleName = ".".join(pieces)
            try:
                module = __import__(moduleName, {}, {}, [attr])
            except:
                raise (AttributeError, """\
%s instance has no attribute '%s', and HasFriends failed too""" % 
                       (self.__class__.__name__, attr))
            f = getattr(module, attr)
            curry = Curry(f, self)
            cache[attr] = curry
        return cache[attr]
