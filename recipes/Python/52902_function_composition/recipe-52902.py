class compose:
    '''compose functions. compose(f,g,x...)(y...) = f(g(y...),x...))'''
    def __init__(self, f, g, *args, **kwargs):
        self.f = f
        self.g = g
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        return self.f(self.g(*args, **kwargs), *self.pending, **self.kwargs)


class mcompose:
    '''compose functions. mcompose(f,g,x...)(y...) = f(*g(y...),x...))'''
    TupleType = type(())

    def __init__(self, f, g, *args, **kwargs):
        self.f = f
        self.g = g
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        mid = self.g(*args, **kwargs)
	if isinstance(mid, self.TupleType):
            return self.f(*(mid + self.pending), **self.kwargs)
        return self.f(mid, *self.pending, **self.kwargs)
