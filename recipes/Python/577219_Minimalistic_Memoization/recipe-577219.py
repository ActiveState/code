def fib(n):
    if n==1 or n==0:
        return 1
    return fib(n-2) + fib(n-1)


def memoize(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf

fib = memoize(fib)
print fib(969)
