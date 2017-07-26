import sys
def exceptional(func,alt_return=None,alt_exceptions=(Exception,),final=None,catch=None):
    """turns exceptions into alternative return value"""
    def _exceptional(*args,**kwargs):
        try:
            try: return func(*args,**kwargs)
            except alt_exceptions:
                return alt_return
            except:
                if catch: return catch(sys.exc_info(), lambda:func(*args,**kwargs))
                raise
        finally:
            if final: final()
    return _exceptional

def final(func,final=None,catch=None,alt_exceptions=(),alt_return=None):
    """connects a final call to a function call"""
    def _exceptional(*args,**kwargs):
        try:
            try: return func(*args,**kwargs)
            except alt_exceptions:
                return alt_return
            except:
                if catch: return catch(sys.exc_info(), lambda:func(*args,**kwargs))
                raise
        finally:
            if final: final()
    return _exceptional

# examples

import os

exceptional( os.mkdir )('log')
print exceptional( list.index )([1,2,3], 4)      # None
print exceptional( list.index, -1 )([1,2,3], 4)  # -1
print exceptional( lambda:open('?').read(),      # :-(
                   ':-(',
                   (OSError,IOError)) ()

open_e = exceptional(open)
f=open_e('first.txt') or open_e('second.txt') or open('third.txt')
s = final(f.read, f.close) ()

class X:
    def f(self):
        return 1/0
    f=exceptional(f,-1)
    @exceptional
    def g(self):
        return 1/0
    def h(self):
        return final(lambda:self.myattr,
                     catch=lambda exc,again:self.create() or again()) ()
    def create(self):
        self.myattr=1

print X().f()
print X().g()
print X().h()
