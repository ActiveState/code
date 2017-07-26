from types import ModuleType, FunctionType
from collections import ChainMap

class _NSChainedDict(ChainMap, dict):
    pass

class Namespace(type):
    def __new__(meta, name, bases, dict):
        mod = ModuleType(name, dict.get("__doc__"))
        for key, obj in dict.items():
            if isinstance(obj, FunctionType):
                obj = meta.chained_function(meta, obj, mod)
            mod.__dict__[key] = obj
        return mod
    def chained_function(meta, func, mod):
        d = _NSChainedDict(mod.__dict__, func.__globals__)
        newfunc = FunctionType(func.__code__, d)
        newfunc.__doc__ = func.__doc__
        newfunc.__defaults__ = func.__defaults__
        newfunc.__kwdefaults__ = func.__kwdefaults__
        return newfunc


# === Test code ===

a = 999
b = 4

def spam(n=None):
    raise RuntimeError('no spam for you!')

class meals(metaclass=Namespace):
    a = 2
    def repeat(word, count):
        return ' '.join([word]*count)
    def ham(n=1):
        return repeat('ham', n)
    def spam(n=3):
        return repeat('spam', n)
    def breakfast():
        """Return yummy and nutritious breakfast"""
        template = "%s with a fried egg on toast and %s"
        return template % (spam(), spam(1))
    def lunch():
        """Return delicious and healthy lunch"""
        template = "cheese, tomato and %s sandwiches"
        return template % spam(a)
    def dinner():
        """Return tasty and wholesome dinner"""
        template = "roast %s garnished with %s"
        return template % (ham(), spam(b))


assert meals.breakfast() == 'spam spam spam with a fried egg on toast and spam'
assert meals.lunch() == 'cheese, tomato and spam spam sandwiches'
assert meals.dinner() == 'roast ham garnished with spam spam spam spam'
