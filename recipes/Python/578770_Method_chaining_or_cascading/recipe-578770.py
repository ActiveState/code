try:
    callable
except NameError:
    # Python 3.0 or 3.1, sigh.
    def callable(obj):
        return hasattr(type(obj), '__call__')

class chained:
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return repr(self.obj)
    def __getattr__(self, name):
        attr = getattr(self.obj, name)
        if callable(attr):
            def selfie(*args, **kw):
                # Call the method just for side-effects, return self.
                _ = attr(*args, **kw)
                return self
            return selfie
        else:
            return attr
