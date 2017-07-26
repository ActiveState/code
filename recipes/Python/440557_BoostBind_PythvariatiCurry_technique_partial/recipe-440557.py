class placeholder(object):
    def __init__(self, pos):
        self.pos = pos

_1 = placeholder(0)
_2 = placeholder(1)
_3 = placeholder(2)

# etc... would be nice to have code to generate N placeholders automatically. 
# is eval the way to do it?
#>>> (Update) see George's comment for an answer to 
#>>> the above question and and alternative solution

def bind(foo, *boundargs, **boundkw):
    """ Allows binding some of the function's args, using placeholders _1, _2,
    etc for the args that are NOT bound (or curried, if you like)
    ========= FOOD FOR DOCTEST ===========
    >>> def foo(a, b, c, d = None, e = None): return (a, b, c, d, e)
    >>> foo(1, 2, 3, e = 'Nooo!')
    (1, 2, 3, None, 'Nooo!')
    >>> foo1 = bind(foo, _2, 2, _1, e = 'Nee!')
    >>> foo1(1, 3)
    (3, 2, 1, None, 'Nee!')
    Test overriding the bound args with the calltime args
    >>> foo1(1, 3, e = 'Overritten')
    (3, 2, 1, None, 'Overritten')
    """
    def with_bound_args(*a, **kw):
        args = []
        for arg in boundargs:
            if isinstance(arg, placeholder):
                args.append(a[arg.pos])
            else:
                args.append(arg)
        #>>> (Update) Peter Harris (PEP 309) mentioned
        #>>> that it makes much more sense to override
        #>>> the bound keyword args with call-time args;
        #>>> hence we have to make a copy of the bound
        #>>> dict and update it, rather than updatinng the 
        #>>> call-time keyword arg dictionary. I agree
        #>>> with the point, although there is an alternative
        #>>> of treating it as an error. The more lenient 
        #>>> way seems more Pythonic.
        kwdict = boundargs.copy()
        kwdict.update(kw)
        return foo(*args, **kwdict)
    return with_bound_args

#>>> Update: I thought about this a little bit longer, especially considering 
#>>> George's observation that this technique is an implementation of 
#>>> 'partial function application' rather that just 'curry'. In languages where
#>>> 'partial application' or 'curry' is supported natively it is possible to 
#>>> just use the name of the function to create a function with partially 
#>>> applied agruments. Well, why not do it in Python? All it takes is a 
#>>> decorator. The decorator decides whether a regular call or a partial 
#>>> application is desired by looking for placeholders in the argument list.

def partial_application(foo):
    def inner(*a, **kw):
        if True in [isinstance(o, placeholder) for o in a]:
            return bind(foo, *a, **kw)
        else: return foo(*a, **kw)
    return inner

@partial_application
def pa_test(a, b, c, d, e = None, f = None):
    """ ============ DOCTEST FOOD ============
    >>> pa_test(1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5, None)
    >>> pa = pa_test(_1, 2, 3, 4, 5)
    >>> pa(1)
    (1, 2, 3, 4, 5, None)
    """
    return (a, b, c, d, e, f)
