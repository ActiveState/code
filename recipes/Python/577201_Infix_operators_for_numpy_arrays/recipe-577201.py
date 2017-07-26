import numpy as np

class Infix(np.ndarray):
    """
    Creates a new infix operator that correcly acts on numpy arrays and scalars, used as X *op* Y.
    The main motivation is to use np.dot as an infix operator for matrix multiplication.

    example:
    >>> x = np.array([1, 1, 1])
    >>> x *dot* x
    3
    >>> 1 + x *dot* x   # Multiplication has higher precedence than addition
    4
    """
    def __new__(cls, function):
        obj = np.ndarray.__new__(cls, 0)
        obj.function = function
        return obj
    def __array_finalize__(self, obj):
        if obj is None: return
        self.function = getattr(obj, 'function', None)
    def __rmul__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __mul__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    
dot = Infix(np.dot)
outer = Infix(np.outer)
