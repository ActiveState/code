"""This file contains the AutomaticClass class."""


class AutomaticClass:

    """This is a base class for simple, struct-like classes."""

    def __init__(self, **kargs):
        """Subclasses should call this after initializing any defaults.

        **kargs - Set each attribute with the given value.  Keys in kargs that
        aren't in self.__attributes__ will be ignored.  

        """
        for i in self.__attributes__:
            if kargs.has_key(i):
                setattr(self, i, kargs[i])

    def getAttributes(self):
        """Return the list of attributes that this class uses.
        
        Subclasses should extend (not override) this method to add their own
        attributes.
        
        """ 
        return []

    def __getattr__(self, attribute):
        """Handle the following attributes manually:  __attributes__.
        
        Meta, meta, meta!
        
        """
        if attribute == "__attributes__":
            return self.getAttributes()
        raise AttributeError

    def __repr__(self):
        """Return a suitable string representing of this instance."""
        attributes = []
        for i in self.__attributes__:
            try: 
                value = getattr(self, i)
            except: 
                value = "Undefined"
            attributes.append("%s=%s" % (i, value))
        return "<%s %s>" % (self.__class__.__name__, " ".join(attributes))


# This is for testing.
class _Test(AutomaticClass):
    def __init__(self, **kargs):
        self.foo = "Bar"
        AutomaticClass.__init__(self, **kargs)
    def getAttributes(self):
        return AutomaticClass.getAttributes(self) + ["foo"]


# Do some testing.
if __name__ == '__main__': 
    assert `_Test()` == "<_Test foo=Bar>"
    assert _Test().foo == "Bar"
    assert _Test(foo = "Not bar").foo == "Not bar"
