from fractions import Fraction

def spread(count, start, end=None, step=None, mode=1):
    if end is step is None:
        raise TypeError('one of end or step must be given')
    if not isinstance(mode, int):
        raise TypeError('mode must be an int')
    if count != int(count):
        raise ValueError('count must be an integer')
    elif count <= 0:
        raise ValueError('count must be positive')
    if mode & 1:
        yield start
    if end is None:
        step = Fraction(step)
        end = start + count*step
    else:
        step = Fraction(end-start)/count
    start = Fraction(start)
    for i in range(1, count):
        yield float(start + i*step)
    if mode & 2:
        yield float(end)
