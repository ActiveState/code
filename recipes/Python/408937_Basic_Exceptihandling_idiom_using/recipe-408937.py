#!/usr/bin/python2.4

# An exception handling idiom using decorators.

__author__ = "Anand Pillai"

def ExpHandler(*posargs):

    def nestedhandler(func,exptuple, *pargs, **kwargs):
        """ Function that creates a nested exception handler from
        the passed exception tuple """

        exp, handler = exptuple[0]
        try:
            if len(exptuple)==1:
                func(*pargs, **kwargs)
            else:
                nestedhandler(func,exptuple[1:], *pargs, **kwargs)
        except exp, e:
            if handler:
                handler(e)
            else:
                print e.__class__.__name__,':',e                
        
    def wrapper(f):
        def newfunc(*pargs, **kwargs):
            if len(posargs)<2:
                t = tuple(item for item in posargs[0] if issubclass(item,Exception) or (Exception,))
                try:
                    f(*pargs, **kwargs)
                except t, e:
                    print e.__class__.__name__,':',e
            else:
                t1, t2 =posargs[0], posargs[1]
                l=[]
                for x in xrange(len(t1)):
                    try:
                        l.append((t1[x],t2[x]))
                    except:
                        l.append((t1[x],None))

                # Reverse list so that exceptions will
                # be caught in order.
                l.reverse()
                t = tuple(l)
                nestedhandler(f,t,*pargs,**kwargs)
                    
        return newfunc

    return wrapper

def myhandler(e):
    print 'Caught exception!', e
    
# Examples
# Specify exceptions in order, first one is handled first
# last one last.
@ExpHandler((ZeroDivisionError,ValueError), (None,myhandler))
def f1():
    1/0

@ExpHandler((TypeError, ValueError, StandardError), (myhandler,)*3)
def f2(*pargs, **kwargs):
    print pargs
    x = pargs[0]
    y = x[0]
    y += x[1]

@ExpHandler((ValueError, Exception))
def f3(*pargs):
    l = pargs[0]
    return l.index(10)

if __name__=="__main__":
    f1()
    # Calls exception handler
    f2('Python', 1)
    # Calls exception handler
    f3(range(5),)
    
