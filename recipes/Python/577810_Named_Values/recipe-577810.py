class NamedValue:
    # defining __slots__ in a mixin doesn't play nicely with builtin types
    # so a low overhead approach would have to use collections.namedtuple
    # style templated code generation
    def __new__(cls, *args, **kwds):
        name, *args = args
        self = super().__new__(cls, *args, **kwds)
        self._name = name
        return self
    def __init__(self, *args, **kwds):
        name, *args = args
        super().__init__(*args, **kwds)
    @property
    def __name__(self):
        return self._name
    def __repr__(self):
        # repr() is updated to include the name and type info
        return "{}({!r}, {})".format(type(self).__name__,
                                     self.__name__,
                                     super().__repr__())
    def __str__(self):
        # str() is unchanged, even if it relies on the repr() fallback
        base = super()
        base_str = base.__str__
        if base_str.__objclass__ is object:
            return base.__repr__()
        return base_str()

# Example usage
>>> class NamedFloat(NamedValue, float):
...     pass
... 
>>> import math
>>> tau = NamedFloat('tau', 2*math.pi)
>>> tau
NamedFloat(tau, 6.283185307179586)
>>> print(tau)
6.283185307179586

>>> class NamedList(NamedValue, list):
...     pass
... 
>>> data = NamedList('data', [])
>>> data
NamedList('data', [])
>>> print(data)
[]
