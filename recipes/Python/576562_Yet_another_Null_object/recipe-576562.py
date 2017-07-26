__all__ = ['Null']

class NullType(object):
    '''An SQL-like Null object: allows most (if not all) operations on it to succeed.

    >>> repr(Null)
    '(Null)'
    >>> Null(3,x=3)
    (Null)
    >>> [Null==Null, Null!=None, Null<Null, Null>=3]
    [(Null), (Null), (Null), (Null)]
    >>> [Null[3], Null.foo]
    [(Null), (Null)]
    >>> Null[4] = 3
    >>> del Null['bar']
    >>> 2.5*Null + 3
    (Null)
    >>> [4 not in Null, 'all' in Null]
    [True, False]
    >>> list(Null)
    []
    >>> bool(Null)
    False
    >>> len(Null)
    0
    >>> [int(Null), long(Null), float(Null), complex(Null)]
    [0, 0, 0.0, 0j]
    >>> [oct(Null), hex(Null)]
    ['(Null)', '(Null)']
    >>> type(Null)() is Null
    True
    >>> from pickle import dumps, loads
    >>> loads(dumps(Null)) is Null
    True
    '''
    __singleton = None
    def __new__(cls, *args, **kwds):
        assert __name__ == '__main__', __name__
        if cls.__singleton is None:
            cls.__singleton = super(NullType,cls).__new__(cls)
        return cls.__singleton
    def __len__(self): return 0
    def __iter__(self): return; yield
    def __nonzero__ (self): return False
    def __contains__(self, item): return False
    def __repr__(self): return '(Null)'
    def __reduce__(self): return (type(self), ())
    __oct__ = __hex__ = __repr__
    __int__ = __long__ = __len__
    def __float__(self): return 0.0
    def __call__(self, *args, **kwds): return self
    __getitem__ = __getattr__ = __setitem__ = __setattr__ = __delitem__ = \
        __delattr__ = __eq__ = __ne__ = __gt__ = __ge__ = __lt__ = __le__ = \
        __neg__ = __pos__ = __abs__ = __invert__ = __add__ = __sub__ = \
        __mul__ = __div__ = __truediv__ = __floordiv__ = __mod__ = \
        __divmod__ = __pow__ = __lshift__ = __rshift__ =  __and__ = __or__ = \
        __xor__ = __radd__ = __rsub__ = __rmul__ = __rdiv__ = __rtruediv__ = \
        __rfloordiv__ = __rmod__ = __rdivmod__ = __rpow__ = __rlshift__ = \
        __rrshift__ = __rand__ = __ror__ = __rxor__ = __call__


Null = NullType()

if __name__ == '__main__':
    from doctest import testmod
    testmod()
