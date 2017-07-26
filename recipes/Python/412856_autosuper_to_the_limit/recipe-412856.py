def automethodinfo(self=None,level=0):
    """
    Return a tuple (cls,self,method), where
    - cls is the class in wich you can find the definition of the method from which this function is called;
    - self is the instance passed as first argument to the method from which this function is called;
    - method is the unbound method from wich this function is called.
    If self is not None, the passed argument is used instead of the instance passed as first argument to the method in which this function is called.
    Pass to level an integer > 0 if you call this from a function nested in the method definition body.
    """
    from inspect import stack

    frame = stack()[level+1][0]
    code = frame.f_code
    name = code.co_name
    self = self or frame.f_locals[code.co_varnames[0]]

    cls = None

    f = None
    for c in type(self).__mro__:
        func_obj = f
        try:
            f = getattr(c,name)
            func_code = f.func_code
        except AttributeError:
            func_code = None

        if func_code is code:
            cls = c
        elif cls is not None:
            break

    if cls is None:
        raise TypeError, "Can only call 'automethodinfo' in a bound method"

    return cls,self,func_obj

def myclass(self=None,level=0):
    """Return the first item returned by automethodinfo."""
    return automethodinfo(self,level+1)[0]

def smartsuper(self=None,level=0):
    """Return a super object to which are passed the proper class and instance for the method from which this function is called. It uses automethodinfo to deduce theese arguments."""
    info = automethodinfo(self,level+1)
    return super(info[0],info[1])

def supermethod(self=None,level=0):
    """Return the bound method with the same name as the module from which this function is called, but defined in the next class found in the mro."""
    
    info = automethodinfo(self,level+1)
    return getattr(super(info[0],info[1]),info[2].func_name)

def autosuper(*a,**k):
    """Execute and get the return value from the bound method with the same name as the module from which this function is called, but defined in the next class found in the mro."""
    return supermethod(level=1)(*a,**k)

## TEST

class A(object):
    def __init__(self):
        print automethodinfo()
        autosuper()
    def foo(self):
        print automethodinfo()

class B1(A):
    def __init__(self):
        print automethodinfo()
        autosuper()
    def foo(self):
        autosuper()
        print automethodinfo()

class B2(A):
    def __init__(self):
        autosuper()
        print automethodinfo()
    def foo(self):
        print automethodinfo()
        autosuper()

class C(B1,B2):
    def __init__(self):
        print automethodinfo()
        autosuper()
    def foo(self):
        print automethodinfo()
        autosuper()
        
c=C()
print "---------"
c.foo()

##    OUTPUT:
##    (<class '__main__.C'>, <__main__.C object at 0x00B83AD0>, <unbound method C.__init__>)
##    (<class '__main__.B1'>, <__main__.C object at 0x00B83AD0>, <unbound method B1.__init__>)
##    (<class '__main__.A'>, <__main__.C object at 0x00B83AD0>, <unbound method A.__init__>)
##    (<class '__main__.B2'>, <__main__.C object at 0x00B83AD0>, <unbound method B2.__init__>)
##    ---------
##    (<class '__main__.C'>, <__main__.C object at 0x00B83AD0>, <unbound method C.foo>)
##    (<class '__main__.B2'>, <__main__.C object at 0x00B83AD0>, <unbound method B2.foo>)
##    (<class '__main__.A'>, <__main__.C object at 0x00B83AD0>, <unbound method A.foo>)
##    (<class '__main__.B1'>, <__main__.C object at 0x00B83AD0>, <unbound method B1.foo>)
