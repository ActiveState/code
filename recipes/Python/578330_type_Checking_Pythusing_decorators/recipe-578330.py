""" 
File checkparams.py
Version 2.0
Written by ll.snark 

Type Checking in Python using decorators
Use the decorator checkparams to check (only unnamed) parameters type
Use the decorator checkreturn to check a return value type :

@checkreturn(int)
@checkparams(int,int)
def ajoute(a,b) :
    if a<0 : return "No negative numbers"
    return a+b

Then Try : 
ajoute(5,6)
ajoute(5,"Argh")
ajoute(-4,6)

Version 2.0 
(
with help from ActiveState members... :
    -better type checking
    -removed unused lines
    -used functools.wraps to copy __name__ and __doc__
)

Note that the preceding decorated function checks if the parameters are
type int or a subtype of int (this is a different behaviour from version 1, 
but I think it's better)
Consequently, you can check only the second parameter, for instance, writing :
@checkparams(object,int)  
def ajoute(a,c) :
    ...
Indeed, type of parameter a will always be a subclass of object.
"""
import functools
def checkparams(*params) :
    def decorator(fonc) :
        @functools.wraps(fonc)
        def foncm(*pnn,**pn) :
            for i,par in enumerate(zip(pnn,params)) :
                if not isinstance(par[0],par[1]) :
                    raise TypeError(foncm.__name__+" Param "+str(i)+" ("+str(par[0])+") is not "+str(par[1]))
            r=fonc(*pnn,**pn)
            return r
        return foncm
    return decorator

def checkreturn(tor) :
    def decorator(fonc) :
        @functools.wraps(fonc)
        def foncm(*pnn,**pn) :
            r=fonc(*pnn,**pn)
            if not isinstance(r,tor) :
                print(type(r))
                raise TypeError(foncm.__name__+" : Return value ("+str(r)+") is not "+str(tor))                
            return r
        return foncm
    return decorator

if __name__=='__main__' : 

    @checkreturn(int)
    @checkparams(int,int)
    def ajoute(a,b) :
        """ Just a sample function to test decorators. """
        if a<0 : return "No negative numbers"
        return a+b


    print(ajoute(5,6))
    print(ajoute(0,"foo"))
    print(ajoute(-3,4))
