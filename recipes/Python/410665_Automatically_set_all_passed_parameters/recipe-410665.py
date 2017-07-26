#The old way:
class Old:
    def __init__(self, a, b, c, d, e, f, g, h, i=200, j=100):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i
        self.j = j


#The new way:

def setargstoself(inst, params):
    code = inst.__init__.func_code
    for item in code.co_varnames[1:code.co_argcount]:
        setattr(inst, item, params[item])

class FooBar:
    def __init__(self, a, b, c, d, e, f, g, h, i=200, j=100)
        setargstoself(self, locals())

fb = FooBar(*range(9)) #set i, leave j as default


#An alternative implementation for functions with arguments *x or **y.
#However, this is less useful, because it would just be another 2 lines to
#assign each one of those to self.
#Here it is if anyone is interested.

import inspect

def setargstoself2(inst, params):
    formal_args, var_args, kwd_args, unused = inspect.getargspec(inst.__init__)
    for item in formal_args:
        if item != 'self':
            setattr(inst, item, params[item])
    if var_args:
        setattr(inst, var_args, params[var_args])
    if kwd_args:
        setattr(inst, kwd_args, params[kwd_args])

class FooBar2:
    def __init__(self, a, b, c, *x, **y):
        setargstoself2(self, locals())

fb2 = FooBar2(name='chloe', name2 = 'sam', *range(6))
