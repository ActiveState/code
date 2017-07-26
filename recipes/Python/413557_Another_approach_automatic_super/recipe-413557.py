from inspect import ismethod
from threading import local

class __current_class(local):
    """current.info is a tuple that, in each thread, contains information about the method that is currently executing and the class in which its definition 

is.

    The tuple is (cls,self,methodname,args,kwargs), where:
    cls is the class in which the method's definition is;
    self is the cls instance passed to the method as its first argument;
    methodname is the name of the method;
    args is the argument tuple passed to the method;
    kwargs is a dictionary of keyword arguments passed to the method.
    """
    def __init__(self):
        local.__init__(self)
        self.info = (None,None,"",(),{})

current = __current_class() # see __current_class doc

class auto(type):
    """auto instances are classes that can mantain information about the method that is currently executing in a certain thread."""
    def __init__(cls,name,bases,dct):
        # returns a function that will replace 'method' so that its execution will update current.info, and then the original method will be called (and its 

result returned).
        def newmethod(method,name):
            def _newmethod(self,*a,**k):
                old_currentinfo = current.info
                current.info = (cls,self,name,a,k) # update current.info
                rv = method(self,*a,**k) # call the original method
                current.info = old_currentinfo # reset current.info to the state in which it was before executing the method
                return rv
            _newmethod.__name__ = method.__name__
            return _newmethod
        # I didn't use inspect.getmembers because I'm just iterating over the methods actually defined in the class body, not over the inherited ones.
        for name in dct:
            m = getattr(cls,name)
            if ismethod(m):
                    setattr(cls,name,newmethod(m,name)) # subclass the method m with the function returned by newmethod (see comments for newmethod)

def upobject():
    """Return super(cls,self), where cls and self are alements of current.info."""
    cls,self = current.info[:2]
    return super(cls,self)

def upmethod():
    """Return upobject().METHOD, where METHOD is the name of the method that is currently executing."""
    return getattr(upobject(),current.info[2])

def upcall(*a,**k):
    """Shortcut for upmethod()(*a,**k)."""
    return upmethod()(*a,**k)

def delegate():
    """Execute and returns the result of upcall(*args,**kwargs) , where args and kwargs are elements of current.info ."""
    a,k = current.info[3:]
    return upmethod()(*a,**k)

class __up_class(object):
    """up is a light wrapper for the super object returned by upobject() . 'up.x' is the same as 'upobject().x' ; 'up.x=y' is the same as 'upobject().x=y."""
    def __getattribute__(self,name):
        return getattr(upobject(),name)
    def __setattr__(self,name,value):
        setattr(upobject(),name,value)

up = __up_class() # see __up_class doc

### TEST ###

from threading import Thread

class A:
    __metaclass__ = auto
    x = "A.x"
    def foo(self,x):
        print "A.foo(%s,%s) ; A.x = %s ;\n\tcurrent.info = %s"%(self,x,A.x,current.info)

class B(A):
    x = "B.x"
    def foo(self,x):
        delegate()
        print "B.foo(%s,%s) ; up.x = %s ;\n\tcurrent.info = %s"%(self,x,up.x,current.info)

class C(A):
    x = "C.x"
    def foo(self,x):
        print "C.foo(%s,%s) ; up.x = %s ;\n\tcurrent.info = %s"%(self,x,up.x,current.info)
        upcall(x*10)

class D(B,C):
    x = "C.x"
    def foo(self,x):
        print "D.foo(%s,%s) ; up.x = %s ;\n\tcurrent.info = %s"%(self,x,up.x,current.info)
        delegate()

d = D()
d.foo(10)

##    OUTPUT:
##
##    D.foo(<__main__.D object at 0x00BAD0F0>,10) ; up.x = B.x ;
##            current.info = (<class '__main__.D'>, <__main__.D object at 0x00BAD0F0>, 'foo', (10,), {})
##    C.foo(<__main__.D object at 0x00BAD0F0>,10) ; up.x = A.x ;
##            current.info = (<class '__main__.C'>, <__main__.D object at 0x00BAD0F0>, 'foo', (10,), {})
##    A.foo(<__main__.D object at 0x00BAD0F0>,100) ; A.x = A.x ;
##            current.info = (<class '__main__.A'>, <__main__.D object at 0x00BAD0F0>, 'foo', (100,), {})
##    B.foo(<__main__.D object at 0x00BAD0F0>,10) ; up.x = C.x ;
##            current.info = (<class '__main__.B'>, <__main__.D object at 0x00BAD0F0>, 'foo', (10,), {})
