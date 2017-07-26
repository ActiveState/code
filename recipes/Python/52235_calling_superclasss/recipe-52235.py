class CallbaseError(AttributeError):
    pass

def callbase(obj, base, methodname='__init__', args=(), raiseIfMissing=None):
    try: method = getattr(base, methodname)
    except AttributeError: 
        if raiseIfMissing:
            raise CallbaseError, methodname
        return None
    if args is None: args = ()
    return method(obj, *args)

# an example: ensure __init__ is called w/o args on _all_ bases
# (if present; ignore no-such-method issues)
class A(B, C, D, E):
    def __init__(self):
        for base in A.__bases__:
            callbase(self, base)
        # class-A-specific initialization here
        self.cachePlokki = {}
# another typical use case: override a method in some base,
# also providing some other stuff around it; e.g. for cache
# on-demand purposes
    def getPlokki(self, *args):
        try: return self.cachePlokki[args]
        except IndexError: pass
        for base in self.__class__.__bases__:
            try: result=callbase(self, base, 'getPlokki', args, 1)
            except CallbaseError: pass
            else: break
        # ok to raise here if result still not bound
        self.cachePlokki[args] = result
        return result
