import sys

__all__ = ["__CHECKING__","throws", "catches"]

__CHECKING__ = True  # (de)activate checking. 

def re_raise(exc, msg, traceback):
    raise exc, msg, traceback

class UncheckedExceptionError(Exception):pass

class ExceptionChecker(object):
    def __init__(self):
        self._id = 0
        self._exceptions = {}
        
    def set_attention(self, exc):
        self._id +=1
        try:                
            self._exceptions[exc].append(self._id)
        except KeyError:
            self._exceptions[exc] = [self._id]
        return self._id            
            
    def remove_attention(self, exc, id):
        try:
            self._exceptions[exc].remove(id)
        except (KeyError, AttributeError):
            pass
        
    def throwing(self, exc):        
        if not self._exceptions.get(exc):            
            raise UncheckedExceptionError(exc)
        
exc_checker = ExceptionChecker()

def catches(exc, handler = re_raise):
    '''
    Function decorator. Used to decorate function that handles exception class exc.
    
    An optional exception handler can be passed as a second argument. This exception
    handler shall have the signature
            handler(exc, message, traceback).
    '''
    if not __CHECKING__:
        return lambda f:f    
    def wrap(f):
        def call(*args, **kwd):            
            try:
                ID = exc_checker.set_attention(exc)
                res = f(*args,**kwd)
                exc_checker.remove_attention(exc, ID)
                return res
            # handle checked exception
            except exc, e:
                exc_checker.remove_attention(exc, ID)
                traceback = sys.exc_info()[2]                                                    
                return handler(exc, str(e), traceback.tb_next.tb_next)
            # re-raise unchecked exception but remove checked exeption info first
            except Exception, e:   
                exc_checker.remove_attention(exc, ID)
                traceback = sys.exc_info()[2]                                                                    
                raise e.__class__, e.args, traceback.tb_next.tb_next                
        call.__name__ = f.__name__
        return call
    return wrap

def throws(exc):
    '''
    throws(exc)(func) -> func'
    
    Function decorator. Used to decorate a function that raises exc.
    '''
    if not __CHECKING__:
        return lambda f:f
    def wrap(f):        
        def call(*args, **kwd):
            res = f(*args,**kwd)
            # raise UncheckedExceptionError if exc is not automatically 
            # registered by a function decorated with @catches(exc);
            # otherwise do nothing
            exc_checker.throwing(exc)  
            return res
        call.__name__ = f.__name__
        return call    
    return wrap

#
#
#  Test
#
# 

def test():
    @throws(ZeroDivisionError)
    def divide(x,y):
       return x/y

    def test1():     # uses divide() but does not implement exception handling
        return divide(2,7)

    try:
       test1()
    except UncheckedExceptionError, e:
       print "Raises UncheckedExceptionError(%s) -> OK"%str(e)

    @catches(ZeroDivisionError)   
    def test2(x,y):     
        return divide(x,y)  # uses divide() correctly. Uses default exception
                            # handler that re-raises the same exception
    assert test2(4,2) == 2

    try:
       test2(1,0)
    except ZeroDivisionError:
       print "Raises ZeroDivisionError -> OK"

    @catches(ZeroDivisionError, handler = lambda exc, msg, traceback: "zero-div")   
    def test3(x,y):     
        return divide(x,y)  # defining handler that returns string "zero-div"
                            # when division by zero 
    assert test3(1,0) == "zero-div"
    
    # declaring two exceptions
    @throws(TypeError)
    @throws(ZeroDivisionError)
    def divide(x,y):
       return x/y 

    try:
        test2(3,2)
    except UncheckedExceptionError, e:
        print "Raises UncheckedExceptionError(%s) -> OK"%str(e)

    @catches(TypeError)   
    @catches(ZeroDivisionError)   
    def test4(x,y):     
        def indirection(x,y):      # indirect call permitted  
            return divide(x,y)     
        return indirection(x,y)
                            
    assert test4(4,2) == 2
