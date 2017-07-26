import inspect

class Deferred(object):
    def __init__(self, expr):
        self.expr = expr

def revaluatable(func):
    varnames,_,_,defaults = inspect.getargspec(func)
    num_varnames = len(varnames); num_defaults = len(defaults)
    def wrapper(*args, **kwds):
        if len(args) >= num_varnames: # defaults not used here
            return func(*args,**kwds)
        f_locals = dict(zip(varnames,args))
        # maximum number of used defaults
        max_defaults = min(num_defaults, num_varnames-len(args))
        for var,default in zip(varnames[-max_defaults:],defaults[-max_defaults:]):
            if var in kwds: 
                continue    # passed as keyword argument; don't use the default
            if not isinstance(default, Deferred): 
                f_locals[var] = default # non re-evaluatable default
            else:                       # reevaluate default expr. in f_locals
                f_locals[var] = eval(default.expr, func.func_globals, f_locals)
        f_locals.update(kwds)           # add any extra keyword arguments
        return func(**f_locals)
    return wrapper


#======= example ===============================================================    

>>> G = 1   # some global
>>>
>>> @revaluatable
... def f(w, x=Deferred('x**2+G'), y=Deferred('w+x'), z=Deferred('[]'))
...     z.extend([w,x,y]); return z
...
>>> f(3)
[3, 10, 13]
>>> G=3; f(4)
[4, 12, 16]
>>> f(4,5)
[4, 5, 9]
>>> f(-1,1,0)
[-1, 1, 0]
>>> from collections import deque
>>> f(-1, z=deque())
deque([-1, 12, 11])
