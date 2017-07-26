import collections
import itertools

class ForwardIterator(object):
    """Wrapper around iterators that lets you read items in advance.

    A ForwardIterator object is initialized passing an iterator as an argument:

    >>> it = ForwardIterator(range(50))

    Once initialized, it can be used exactly like the original iterator:

    >>> next(it)
    0
    >>> next(it)
    1

    ForwardIterator supports an additional method look_forward() that lets you
    preview future items without exhausting the iterator:

    >>> it.look_forward()
    2
    >>> next(it)
    2

    look_forward() accepts an optional argument: the number of items to read
    ahead. The default value for the argument is 1:

    >>> it.look_forward(1)
    3
    >>> it.look_forward(3)
    5

    """

    __slots__ = '_iterator', '_prefetched'

    def __init__(self, iterable):
        self._iterator = iter(iterable)
        self._prefetched = collections.deque()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._prefetched.popleft()
        except IndexError:
            pass
        try:
            return next(self._iterator)
        except StopIteration:
            # PEP 479 forbids the implicit propagation of StopIteration.
            raise StopIteration

    def look_forward(self, n=1):
        """Read ahead an item without advancing the iterator."""
        if n < 1:
            raise ValueError("'n' must be greater than 0, got %r" % n)
        required = n - len(self._prefetched)
        if required > 0:
            self._prefetched.extend(itertools.islice(self._iterator, required))
        try:
            return self._prefetched[n - 1]
        except IndexError:
            raise StopIteration from None

    def __length_hint__(self):
        return self._iterator.__length_hint__() + len(self._prefetched)


if __name__ == '__main__':
    def assert_raises(exc, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exc:
            pass
        else:
            raise AssertionError

    it = ForwardIterator('abcdefghijklmnopqrstuvwxyz')

    assert it.__length_hint__() == 26
    assert next(it) == 'a'
    assert next(it) == 'b'
    assert it.__length_hint__() == 24

    assert it.look_forward() == 'c'
    assert it.look_forward(1) == 'c'
    assert it.look_forward(2) == 'd'
    assert it.look_forward(16) == 'r'
    assert it.__length_hint__() == 24

    assert_raises(ValueError, it.look_forward, 0)
    assert_raises(ValueError, it.look_forward, -1)
    assert_raises(StopIteration, it.look_forward, 123)

    assert ''.join(it) == 'cdefghijklmnopqrstuvwxyz'
    assert it.__length_hint__() == 0
    assert_raises(StopIteration, next, it)
    assert_raises(StopIteration, it.look_forward)

    import doctest
    doctest.testfile(__file__, globs={'ForwardIterator': ForwardIterator})
