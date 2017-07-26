def any_args(self,*a,**k): return True

def watch_call(method_name,arg_test= any_args):
    """ Adds a Conditionnal Breakpoint to the method method_name of the decorated obj
    """
    def make_watcher(obj): 
        class _watch(obj):
            def __init__(self,*a,**k):
                init= getattr(obj,'__init__',None) 
                if init: return init(self,*a,**k)                
            def _watched_method(self,*a,**k):
                if arg_test(self,*a,**k):
                    This_is_a_breakpoint= True # Put a breakpoint here, or take any other action
                return obj.__dict__[method_name](self,*a ,**k)        
        setattr(_watch,method_name,_watch._watched_method)
        return _watch
    return make_watcher

def _________________tests__________________():pass

@watch_call("f",lambda s,*a,**k: a[0]== 1 )
class test:
    def f(self,x,y= 3):
        print "f(%s)"% (x+y)
    def g(self,x,y=3):
        print "g()"

if __name__== "__main__":
    # BreakPoint if l is appenned a list
    l=  watch_call("append",lambda s,*a,**k: isinstance(a[0],list))(list)()
    l.append('?')
    l.append([])
    print l
    # BreakPoint if d is __setattr__["a"]
    d=  watch_call("__setitem__",lambda s,*a,**k: a[0]== "a" )(dict)()
    d['a']= 1
    print d
    # Decorate class
    t= test()
    t.g(1)
    t.f(1)
    t.g(2)
    t.f(2)
