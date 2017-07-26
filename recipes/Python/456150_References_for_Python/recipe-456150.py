class Ref(object):
    _unbound = object()
    def __new__(cls, value = _unbound):
        """We're an object, but need to ignore the optional argument."""

        return object.__new__(cls)

    def __init__(self, value = _unbound):
        """Bind the  optional value, if provided."""
        if value is not self._unbound:
            self._value = value

    def __pos__(self):
        """Return value, if bound."""
        try:
            return self._value
        except AttributeError:
            raise NameError, "%s object does not have a value stored." % \
                  self.__class__.__name__

    def __iadd__(self, value):
        self._value = value
        return self
