class Singleton(type):
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}

    def __call__(self, *args):
        if not args in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]

class Test:
    __metaclass__=Singleton
    def __init__(self, *args): pass

            
ta1, ta2 = Test(), Test()
assert ta1 is ta2

tb1, tb2 = Test(5), Test(5)
assert tb1 is tb2

assert ta1 is not tb1
