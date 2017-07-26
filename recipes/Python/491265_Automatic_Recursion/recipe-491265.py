# simple dirty trick for automatic recursion: keyword args from locals()

def myfunc(a,b=1,c=2,d=3,e=4):
    _kwargs=locals().copy()    # freeze unconditional at very beginning
    print locals()
    if e<=0: return
    else:
        _kwargs['e']=e-1
        myfunc(**_kwargs)

# proper tools for correct/ad-hoc/fast automatic recursion

def recursion_args(func, func_locals, **kwargs):
    """returns named positional args only - without original *args, **kwargs"""
    co=func.func_code
    return tuple([ kwargs.pop(co.co_varnames[i], func_locals[co.co_varnames[i]])
                   for i in range(co.co_argcount) ])
    assert not kwargs

def recurse(func, func_locals, *args, **kwargs):
    """for ad-hoc recursion - in case: manual insertion of original *args/**kwargs.
    Use it like  recurse(myfunc,locals(),changed=changed-1,*args,**kwargs)"""
    co=func.func_code
    args = tuple([ kwargs.pop(co.co_varnames[i], func_locals[co.co_varnames[i]])
                   for i in range(co.co_argcount) ]) + args
    return func(*args,**kwargs)

def recurse_ex(func, func_locals, **kwargs):
    """auto-handles original *args and **kwargs.
    Use it like recurse_ex(myfunc,locals(),changed=changed-1)
    """
    co=func.func_code
    args = tuple([ kwargs.pop(co.co_varnames[i], func_locals[co.co_varnames[i]])
                   for i in range(co.co_argcount) ])
    if co.co_flags & 0x04:
        i+=1
        args+=func_locals[co.co_varnames[i]]
    if co.co_flags & 0x08:
        kwargs.update(func_locals[co.co_varnames[i+1]]) #TODO:reverse priority?
    return func(*args,**kwargs)

def recursor(func, func_locals):
    co=func.func_code
    def _recursor(**kwargs):
        args=tuple([kwargs.pop(co.co_varnames[i],func_locals[co.co_varnames[i]])
                    for i in range(co.co_argcount) ])
        return func(*args,**kwargs)
    return _recursor

def recursor1(func):
    # for recursion with some pre-computatation; 
    co=func.func_code
    argnames=[ co.co_varnames[i] for i in range(co.co_argcount) ]
    def _recursor1(func_locals,**kwargs):
        return func( *tuple([ kwargs.pop(name,func_locals[name])
                              for name in argnames ]), **kwargs )
    return _recursor1

# examples

def func1(a,b=1,c=2,d=3,e=4):
    print locals()
    if e<=0: return
    else:
        recurse(func1,locals(),
                e=e-1 )               # recurse with e changed

def func2(a,b=1,c=2,d=3,e=4):
    RECURSE=recursor(func2,locals())  # freeze it at the beginning
    print locals()
    if e<=0: return
    else:
        RECURSE(e=e-1)     

def func3(a,b=1,c=2,d=3,e=4):
    print locals()
    if e<=0: return
    else:
        func3_recurse(locals(),
                      e=e-1 )
func3_recurse=recursor1(func3)

def func4(a,b=5,*args,**kwargs):
    _v=1
    print locals()
    if b<=0: return
    else:
        recurse_ex(func4,locals(),
                   b=b-1 )

echo_args=None
def func_with_echo(a,b=1,c=2,d=3,e=4, echo=None):
    print locals()
    global echo_args
    if not echo:
        if echo_args:
            func_with_echo(*echo_args)
        echo_args=recursion_args(func_with_echo, locals(),
                                 echo=1)

class Class:
    def meth(self,a,b=1,c=2):
        print locals()
        if c<=0: return
        else:
            recurse(Class.meth,locals(),
                    c=c-1)

if __name__=='__main__':
    myfunc('myfunc')
    func1('func-1')
    func2('func-2')
    func3('func-3')
    func4('func-4',5,4,3,2,1,extra='e')
    Class().meth('E')
    func_with_echo('first')
    func_with_echo('second',c=7)
