class CF(object):
    'Decorator for creating a composable function'

    def __init__(self, f):
        self.func = f

    def __call__(self, x):
        return self.func(x)
       
    def __getattr__(self, other):
        other = globals()[other]
        return CF(lambda x: self(other(x)))


#-------- Example ----------

@CF
def f(x):
    return 3 * x

@CF
def g(x):
    return x + 10

print (f . g)(2)    # same as f(g(2))
