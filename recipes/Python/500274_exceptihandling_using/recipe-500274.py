import functools
def ExpHandler(*pargs):
    """ An exception handling idiom using decorators"""

    def wrapper(f):
        if pargs:
            (handler,li) = pargs
            t = [(ex, handler)
                 for ex in li ]
            t.reverse()
        else:
            t = [(Exception,None)]

        def newfunc(t,*args, **kwargs):
            ex, handler = t[0]

            try:
                if len(t) == 1:
                    f(*args, **kwargs)
                else:
                    newfunc(t[1:],*args,**kwargs)
            except ex,e:
                if handler:
                    handler(e)
                else:
                    print e.__class__.__name__, ':', e

        return functools.partial(newfunc,t)
    return wrapper
def myhandler(e):
    print 'Caught exception!', e

# Examples
# Specify exceptions in order, first one is handled first
# last one last.

@ExpHandler(myhandler,(ZeroDivisionError,))
@ExpHandler(None,(AttributeError, ValueError))
def f1():
    1/0

@ExpHandler()
def f3(*pargs):
    l = pargs
    return l.index(10)

if __name__=="__main__":
    f1()
    f3()
