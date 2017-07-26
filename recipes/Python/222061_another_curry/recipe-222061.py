#---------------------------------------------------------------curry---
lcurry = lambda func, *args, **kw:\
            lambda *p, **n:\
                func(*args + p, **dict(kw.items() + n.items()))

# just for esthetics...
curry = lcurry


#--------------------------------------------------------------rcurry---
# NOTE: this adds the curried args to the tail...
rcurry = lambda func, *args, **kw:\
            lambda *p, **n:\
                func(*p + args, **dict(kw.items() + n.items()))


#--------------------------------------------------------------LCurry---
class LCurry(object):
    '''
    this is the left curry class.
    '''
    def __new__(cls, func, *args, **kw):
        obj = object.__new__(cls)
        if isinstance(func, LCurry) or isinstance(func, RCurry):
            obj._curry_func = func._curry_func
            obj._curry_args = (func._curry_args[0] + args, func._curry_args[1])
            obj._curry_kw = kw = kw.copy()
            kw.update(func._curry_kw)
        else:
            obj._curry_func = func
            obj._curry_args = (args, ())
            obj._curry_kw = kw.copy()
        return obj
    def __call__(self, *args, **kw):
        self._curry_func(*self._curry_args[0] + args + self._curry_args[1], **dict(self._curry_kw.items() + kw.items()))

# just for esthetics...
Curry = LCurry


#--------------------------------------------------------------RCurry---
class RCurry(object):
    '''
    this is the right curry class.
    '''
    def __new__(cls, func, *args, **kw):
        obj = object.__new__(cls)
        if isinstance(func, LCurry) or isinstance(func, RCurry):
            obj._curry_func = func._curry_func
            obj._curry_args = (func._curry_args[0] ,func._curry_args[1] + args)
            obj._curry_kw = kw = kw.copy()
            kw.update(func._curry_kw)
        else:
            obj._curry_func = func
            obj._curry_args = ((), args)
            obj._curry_kw = kw.copy()
        return obj
    def __call__(self, *args, **kw):
        self._curry_func(*self._curry_args[0] + args + self._curry_args[1], **dict(self._curry_kw.items() + kw.items()))



#-----------------------------------------------------------------------
