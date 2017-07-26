class Property(object):
    class __metaclass__(type):
        def __init__(cls, name, bases, dct):
            for fname in ['get', 'set', 'delete']:
                if fname in dct:
                    setattr(cls, fname, staticmethod(dct[fname]))
        def __get__(cls, obj, objtype=None):
            if obj is None:
                return cls
            fget = getattr(cls, 'get')
            return fget(obj)
        def __set__(cls, obj, value):
            fset = getattr(cls, 'set')
            fset(obj, value)
        def __delete__(cls, obj):
            fdel = getattr(cls, 'delete')
            fdel(obj)
