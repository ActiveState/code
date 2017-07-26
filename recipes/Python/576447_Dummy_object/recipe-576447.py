class Dummy(object):
    def __getattr__(self, attr):
        try:
            return super(self.__class__, self).__getattr__(attr)
        except AttributeError:
            if attr in ('__base__', '__bases__', '__basicsize__', '__cmp__',
                        '__dictoffset__', '__flags__', '__itemsize__',
                        '__members__', '__methods__', '__mro__', '__name__',
                        '__subclasses__', '__weakrefoffset__',
                        '_getAttributeNames', 'mro'):
                raise
            else:
                return self
    def next(self):
        raise StopIteration
    def __repr__(self):
        return 'Dummy()'
    def __init__(self, *args, **kwargs):
        pass
    def __len__(self):
        return 0
    def __eq__(self, other):
        return self is other
    def __hash__(self):
        return hash(None)
    def __call__(self, *args, **kwargs):
        return self
    __sub__ = __div__ = __mul__ = __floordiv__ = __mod__ = __and__ = __or__ = \
    __xor__ = __rsub__ = __rdiv__ = __rmul__ = __rfloordiv__ = __rmod__ = \
    __rand__ = __rxor__ = __ror__ = __radd__ = __pow__ = __rpow__ = \
    __rshift__ = __lshift__ = __rrshift__ = __rlshift__ = __truediv__ = \
    __rtruediv__ = __add__ = __getitem__ = __neg__ = __pos__ = __abs__ = \
    __invert__ = __setattr__ = __delattr__ = __delitem__ = __setitem__ = \
    __iter__ = __call__

Dummy = Dummy()
