from types import CodeType

code_args = (
    'argcount', 'nlocals', 'stacksize', 'flags', 'code',
    'consts', 'names', 'varnames', 'filename', 'name',
    'firstlineno', 'lnotab', 'freevars', 'cellvars'
    )

def copy_code(code_obj, **kwargs):
    "Make a copy of a code object, maybe changing some attributes"
    for arg in code_args:
        if not kwargs.has_key(arg):
            kwargs[arg] = getattr(code_obj, 'co_%s' % arg) 
    return CodeType(*map(kwargs.__getitem__, code_args))

def posonly(f):
    "Make the arguments of a function positional only"
    code = f.func_code
    varnames, nargs = code.co_varnames, code.co_argcount
    varnames = ( tuple(v+'@' for v in varnames[:nargs])
                 + varnames[nargs:] )
    f.func_code = copy_code(code, varnames = varnames)
    return f

#--- Examples of use ---------------------

>>> @posonly
... def f(x, y=1): return x, y
... 
>>> f(1)
(1, 1)
>>> f(1, y=2)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() got an unexpected keyword argument 'y'
>>> f(x=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: f() got an unexpected keyword argument 'x'
>>> @posonly
... def update(self, container=None, **kwargs):
...     "Pretend function"
...     return self, container, kwargs
... 
>>> # self and container can be used as keyword argument names
... update('self', 'container', self=1, container=2)
('self', 'container', {'self': 1, 'container': 2})
>>> # There is still a way to access posonly args by name...
... f(**{'x@':'spam'})
('spam', 1)
>>>
