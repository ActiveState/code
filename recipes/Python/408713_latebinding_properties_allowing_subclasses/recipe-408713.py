class LateBindingProperty(object):
    def __init__(self, getname=None, setname=None, delname=None,
                 doc=None):
        self.getname = getname
        self.setname = setname
        self.delname = delname
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.getname is None:
            raise AttributeError('unreadable attribute')
        try:
            fget = getattr(obj, self.getname)
        except AttributeError:
            raise TypeError('%s object does not have a %s method' %
                            (type(obj).__name__, self.getname))
        return fget()

    def __set__(self, obj, value):
        if self.setname is None:
            raise AttributeError("can't set attribute")
        try:
            fset = getattr(obj, self.setname)
        except AttributeError:
            raise TypeError('%s object does not have a %s method' %
                            (type(obj).__name__, self.setname))
        fset(value)

    def __delete__(self, obj):
        if self.delname is None:
            raise AttributeError("can't delete attribute")
        try:
            fdel = getattr(obj, self.delname)
        except AttributeError:
            raise TypeError('%s object does not have a %s method' %
                            (type(obj).__name__, self.delname))
        fdel()
