"""attributes module"""

class Attribute:
    """A class attribute (non-data descriptor).

    The class provides for an initial value and a docstring.  This
    replaces putting the information in the docstring of the class.

    """

    def __init__(self, value, doc=""):
        self.value = value
        self.docstring = doc
    def __get__(self, obj, cls):
        return self
    def __getattribute__(self, name):
        if name == "__doc__":
            return object.__getattribute__(self, "docstring")
        return object.__getattribute__(self, value)


class AbstractAttribute:
    """An abstract class attribute.

    Use this instead of an abstract property when you don't expect the
    attribute to be implemented by a property.

    """

    __isabstractmethod__ = True

    def __init__(self, doc=""):
        self.__doc__ = doc
    def __get__(self, obj, cls):
        return self
