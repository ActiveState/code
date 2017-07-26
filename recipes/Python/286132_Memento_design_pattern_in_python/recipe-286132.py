class MementoMetaclass(type):    
    cache = {}

    def __call__(self, *args):
        print "="*20
        print "ClassObj:", self
        print "Args:", args
        print "="*20
        cached = self.cache.get(args, None)
        if not cached:
            instance = type.__call__(self, *args)
            self.cache.update({args:instance})
            return instance
        return cached
        
class Foo(object):
    __metaclass__ = MementoMetaclass
    template = ''
    def __init__(self, arg1, arg2, arg3):
        self.template = arg1

a = Foo(1,2,3)
b = Foo(2,3,4)
c = Foo(1,2,3)
d = Foo(2,3,4)
e = Foo(5,6,7)
f = Foo(5,6,7)

print id(a), id(b), id(c), id(d), id(e), id(f)
