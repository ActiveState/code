__docformat__ = "restructuredtext"


class peekable:

    """Make an iterator peekable.

    This is implemented with an eye toward simplicity.  On the downside,
    you can't do things like peek more than one item ahead in the
    iterator.  On the bright side, it doesn't require anything from
    itertools, etc., so it's less likely to encounter strange bugs,
    which occassionally do happen.

    Example usage::

        >>> numbers = peekable(range(6))
        >>> numbers.next()
        0
        >>> numbers.next()
        1
        >>> numbers.peek()
        2
        >>> numbers.next()
        2
        >>> numbers.next()
        3
        >>> for i in numbers:
        ...     print i
        ... 
        4
        5

    """

    _None = ()  # Perhaps None is a valid value.

    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._buf = self._None

    def __iter__(self):
        return self

    def _is_empty(self):
        return self._buf is self._None

    def peek(self):
        """Peek at the next element.

        This may raise StopIteration.

        """
        if self._is_empty():
            self._buf = self._iterable.next()
        return self._buf

    def next(self):
        if self._is_empty():
            return self._iterable.next()
        ret = self._buf
        self._buf = self._None
        return ret


def groupbysorted(iterable, keyfunc=None):

    """This is a variation of itertools.groupby.

    The itertools.groupby iterator assumes that the input is not sorted
    but will fit in memory.  This iterator has the same API, but assumes
    the opposite.

    Example usage::

        >>> for (key, subiter) in groupbysorted(
        ...     ((1, 1), (1, 2), (2, 1), (2, 3), (2, 9)), 
        ...     keyfunc=lambda row: row[0]):
        ...     print "New key:", key
        ...     for x in subiter:
        ...         print "Row:", x
        ... 
        New key: 1
        Row: (1, 1)
        Row: (1, 2)
        New key: 2
        Row: (2, 1)
        Row: (2, 3)
        Row: (2, 9)

    This requires the peekable class.  See my comment here_.

    Note, you must completely iterate over each subiter or groupbysorted will
    get confused.

    .. _here:
       http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/304373

    """

    iterable = peekable(iterable)

    if not keyfunc:
        def keyfunc(x):
            return x

    def peekkey():
        return keyfunc(iterable.peek())

    def subiter():
        while True:
            if peekkey() != currkey:
                break
            yield iterable.next()

    while True:
        currkey = peekkey()
        yield (currkey, subiter())
