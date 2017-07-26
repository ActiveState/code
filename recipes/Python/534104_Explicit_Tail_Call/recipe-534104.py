class TailCall(Exception):
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

def has_tail_calls(f):
    def tail_call_wrapper(*args, **kwargs):
        current_func = f
        while True:
            try:
                return current_func(*args, **kwargs)
            except TailCall, e:
                current_func = getattr(e.f, '_tail_callable', e.f)
                args = e.args
                kwargs = e.kwargs
    tail_call_wrapper._tail_callable = f
    tail_call_wrapper.__doc__ = f.__doc__
    return tail_call_wrapper


@has_tail_calls
def sum_range(n, total=0):
    """Sum the integers from 1 to n.

    Obviously the same as n(n+1)/2, but this is a test, not a demo.

    >>> sum_range(1)
    1
    >>> sum_range(100)
    5050
    >>> sum_range(100000)
    5000050000L
    """
    if not n:
        return total
    else:
        raise TailCall(sum_range, n - 1, n + total)


@has_tail_calls
def fact2(n, v=1):
    """Factorial.

    >>> fact2(1)
    1
    >>> fact2(2)
    2
    >>> fact2(3)
    6
    >>> fact2(4)
    24
    >>> fact2(20)
    2432902008176640000L
    """
    if not n:
        return v
    else:
        raise TailCall(fact2, n - 1, v * n)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
