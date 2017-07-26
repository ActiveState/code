from __future__ import with_statement
from contextlib import contextmanager

@contextmanager
def Switch():
    D = {}

    class _P(Exception): pass
    def _mkCase(var):
        class _PP(_P):
            V = var
            def __repr__(self):
                return str(self.V)
        D[var]=_PP
        return _PP
        
    def switch(var):
        if D.has_key(var):
            raise D[var]()
        raise _mkCase(var)()
    
    def case(var):
        if D.has_key(var):
            return D[var]
        return _mkCase(var)
    def default():
        return _P
        
    yield switch, case, default    
    

if __name__=="__main__":
    def test1():
        with Switch() as (switch, case, default):
            try: switch(55)
            except case(1):
                print 1
            except case(6):
                print 6
            except case(5):
                print 5
            except default():
                print 'default..'
    
    def test2():
        with Switch() as (switch, case, default):
            try:switch('hola')
            except case(1):
                print 1
            except case('holaS'):
                print 'holaS'
            except case('hola'):
                print 'hola'
            except default():
                print 'default..'
                
                
    test1()
    test2()
