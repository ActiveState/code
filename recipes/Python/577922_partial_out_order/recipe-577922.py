from functools import partial
from inspect import getargspec, ismethod

def keywords_first(f):
    def wrapper(*a, **k):
        a = list(a)
        #for idx, arg in enumerate(f.func_code.co_varnames[:f.func_code.co_argcount], -ismethod(f)):
        for idx, arg in enumerate(getargspec(f).args, -ismethod(f)): # or [0] in 2.5
            if arg in k:
                if idx < len(a):
                    a.insert(idx, k.pop(arg))
                else:
                    break
        return f(*a, **k)
    return wrapper

@keywords_first
def fun(a, b, c=3): return a, b, c

print fun(1, 3, b=2) # normally: TypeError: f() got multiple values for keyword argument 'b'

def fun2(a, b, *args, **kwargs): return a, b, args, kwargs

print partial(keywords_first(fun2), a=1, c=2, b=2)(3, 4, 5, 6, 7) # noramlly: TypeError ...

def kfpartial(fun, *args, **kwargs):
    return partial(keywords_first(fun), *args, **kwargs)
   
print kfpartial(fun2, a=1, b=2)(3, 4, 5, 6, 7, c=3)
