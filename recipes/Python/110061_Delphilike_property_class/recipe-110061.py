# "Extended" property class that implements Delphi property logic.
# Its constructor accepts attribute names as well as functions
# for a getter or/and setter parameters thus allowing "direct"
# access to underlying "real" attribute without additional coding.

class xproperty(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        property.__init__(
            self,
            (isinstance(fget, str) and (lambda obj: getattr(obj, fget))
                                   or fget),
            (isinstance(fset, str) and (lambda obj, val: setattr(obj, fset, val))
                                   or fset),
            fdel,
            doc)


# A simple example of xproperty usage.
# The attribute 's' is converted to lowercase when assigned, but reading
# immediately returns the value of the "real" underlying attribute '_s'
# So, setting s ends up calling __sets; getting s simply returns _s

class Lower(object):
    def __init__(self):
        self._s = ''

    def __sets(self, val):
        if isinstance(val, str):
            self._s = val.lower()
        else:
            self._s = val

    s = xproperty('_s', __sets)
