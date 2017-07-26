class Lazy(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value


# Sample use:

class SomeClass(object):

    @Lazy
    def someprop(self):
        print 'Actually calculating value'
        return 13


o = SomeClass()
o.someprop
o.someprop
