class ConvertArgumentTypes(object):
    """Converts function arguments to specified types."""
    def __init__(self,*args, **kw):
        self.args = args
        self.kw = kw
    def __call__(self, f):
        def func(*args, **kw):
            nargs = [x[0](x[1]) for x in zip(self.args, args)]
            invalidkw = [x for x in kw if x not in self.kw]
            if len(invalidkw) > 0:
                raise TypeError, f.func_name + "() got an unexpected keyword argument '%s'" % invalidkw[0]
            kw = dict([(x,self.kw[x](kw[x])) for x in kw])
            v = f(*nargs, **kw)
            return v
        return func

#keyword arguments are handled normally.
@ConvertArgumentTypes(int, float, c=int, d=str)
def z(a,b,c=0,d=""):
    return a + b, (c,d)

@ConvertArgumentTypes(int, int)
def y(p,q):
    return p + q

print y("1","2")

print z(1,2,c=34,d=56)
