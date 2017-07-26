import itertools

def minmax(data):
    'Computes the minimum and maximum values in one-pass using only 1.5*len(data) comparisons'
    it = iter(data)
    try:
        lo = hi = next(it)
    except StopIteration:
        raise ValueError('minmax() arg is an empty sequence')
    for x, y in itertools.izip_longest(it, it, fillvalue=lo):
        if x > y:
            x, y = y, x
        if x < lo:
            lo = x
        if y > hi:
            hi = y
    return lo, hi

if __name__ == '__main__':
    import random
    data = [random.random() for i in range(1000)]
    print minmax(data)
