# flattens a list eg. flatten(1, 2, ['b','a','c']) = [1, 2, 'a', 'b', 'c']
def flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x
