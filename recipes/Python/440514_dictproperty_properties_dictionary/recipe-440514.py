class dictproperty(object):

    class proxy(object):
        def __init__(self, fget, fset, fdel):
            self._fget = fget
            self._fset = fset
            self._fdel = fdel
            self._obj = None

        def setObj(self, obj):
            self._obj = obj

        def __getitem__(self, key):
            if self._fget is None:
                raise TypeError, "can't read item"
            return self._fget(self._obj, key)

        def __setitem__(self, key, value):
            if self._fset is None:
                raise TypeError, "can't set item"
            self._fset(self._obj, key, value)

        def __delitem__(self, key):
            if self._fdel is None:
                raise TypeError, "can't delete item"
            self._fdel(self._obj, key)

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self._proxy = dictproperty.proxy(fget, fset, fdel)
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        self._proxy.setObj(obj)
        return self._proxy
