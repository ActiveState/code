import time
import types

class StrictlyType(object):
    """Returns a strictly typed function"""
    def __init__(self,*args):
        self.args = args
    def __call__(self, f):
        def func(*args):
            for a in zip(self.args, [type(arg) for arg in args]):
                if a[0] is not a[1]:
                    raise TypeError, 'Expected %s, got %s' % a
            v = f(*args)
            return v
        func.func_name = f.func_name
        return func

@StrictlyType(types.IntType, types.FloatType)
def z(a,b):
    return a + b
    
print z(4,5.1)
#9.1

print z(4,5)
#Traceback (most recent call last):
#  File "st.py", line 24, in ?
#    print z(4,5)
#  File "st.py", line 12, in func
#    raise TypeError, 'Expected %s, got %s' % a
#TypeError: Expected <type 'float'>, got <type 'int'>
