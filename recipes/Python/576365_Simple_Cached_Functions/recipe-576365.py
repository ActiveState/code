def cachable(func):
    '''
    Cache results of function in func.cache.
    -- No keyword args allowed.
    '''
    func.cache = {}
    def out(*args):
        if args not in func.cache:
            func.cache[args] = func(*args)
        return func.cache[args]
    return out


# ------------------- test it out --------------------
@cachable
def fibonacci(n):
    if n == 0 or n == 1:
        out = 1
    else:
        out = fibonacci(n - 1) + fibonacci(n - 2)
    return out

import time
start = time.time()
for i in range(35):
    print i, fibonacci(i)
print 'Time:', time.time() - start

# 0.17 Seconds!
