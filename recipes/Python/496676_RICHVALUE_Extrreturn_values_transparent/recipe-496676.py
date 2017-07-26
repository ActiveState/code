# Enriches (return) values transparently with extra data.

def RICHVALUE(v, **kwargs):
    try:
        class _RICHVALUE(type(v)):
            pass
        vv=_RICHVALUE(v)
    except TypeError:
        import copy
        vv=copy.copy(v)
    vv.__dict__.update(kwargs)
    return vv

def f():
    return RICHVALUE(7, extra="hello")

def g():
    class X: pass
    return RICHVALUE(X(), extra="hello")

def h(want_extra=False):
    class Y(object): pass
    y=Y()
    if want_extra:
        return RICHVALUE(y, extra="hello")
    return y

ret=f()
print ret, ret+1, ret.extra
ret=g()
print ret, ret.extra
ret=h(want_extra=True)
print ret, getattr(ret,'extra',"???")
