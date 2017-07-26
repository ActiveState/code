# from recipe 222061
curry = lambda func, *args, **kw:\
            lambda *p, **n:\
                func(*args + p, **dict(kw.items() + n.items()))

# bothmethod as a descriptor/decorator
class bothmethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return curry(self.func, type)
        else:
            return curry(self.func, obj)

# test
class Test(object):
    @bothmethod
    def method(self_or_cls):
        print 'The first argument is: %s' % self_or_cls

# when called on the class, it gets the class
>>> Test.method()
The first argument is: <class '__main__.Test'>

# when called on an instance, it gets that instance
>>> Test().method()
The first argument is: <__main__.Test object at 0xb7d5ad0c>
