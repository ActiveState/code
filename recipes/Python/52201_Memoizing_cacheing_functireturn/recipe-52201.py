# Functions can be memoised "by hand" using a dictionary to hold
# the return values when they are calculated:

# Here is a simple case, using the recursive fibonnaci function
#     f(n) = f(n-1) + f(n-2)

fib_memo = {}
def fib(n):
    if n < 2: return 1
    if not fib_memo.has_key(n):
        fib_memo[n] = fib(n-1) + fib(n-2)
    return fib_memo[n]

# To encapsulate this in a class, use the Memoize class:

class Memoize:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if not self.memo.has_key(args):
            self.memo[args] = self.fn(*args)
        return self.memo[args]

# And here is how to use this class to memoize fib(). Note that the definition
# for fib() is now the "obvious" one, without the cacheing code obscuring
# the algorithm.
def fib(n):
    if n < 2: return 1
    return fib(n-1) + fib(n-2)

fib = Memoize(fib)

# For functions taking mutable arguments, use the cPickle module, as
# in class MemoizeMutable:

class MemoizeMutable:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will work on functions with mutable arguments (slower than Memoize)
    """
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        import cPickle
        str = cPickle.dumps(args)
        if not self.memo.has_key(str):
            self.memo[str] = self.fn(*args)
        return self.memo[str]
