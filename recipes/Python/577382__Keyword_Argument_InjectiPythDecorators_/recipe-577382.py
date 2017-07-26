class RedundantTest:
    def __init__(self, x, y, z, t):
        # Here are the redundant lines:
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        print x,y,z,t

# ===================================

def injectArguments(inFunction):
    def outFunction(*args,**kwargs):
        _self = args[0]
        _self.__dict__.update(kwargs)
        inFunction(*args,**kwargs)
    return outFunction
 
class Test:
    @injectArguments
    def __init__(self, x, y, z, t):
        # We don't have to set each attribute. They're already set by injectArguments
        print self.x,self.y,self.z,self.t
 
    @injectArguments
    def function(self, name):
	print "Name:",self.name
 
t = Test(x=4, y=5, z=6, t=7)
t.function(name="Emre")
